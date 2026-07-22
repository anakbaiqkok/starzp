import asyncio
import hashlib
import json
import os
import random
import re
from collections import OrderedDict
from typing import Dict, List, Optional

import aiofiles
import httpx

from logs import logger


class Bing:
    def __init__(self, cookies_file: str):
        self.cookies = self._load_cookies(cookies_file)
        self.shuffled_cookies = self.cookies.copy()
        random.shuffle(self.shuffled_cookies)
        self.current_index = 0

    def _load_cookies(self, cookies_file: str) -> List[Dict[str, str]]:
        with open(cookies_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_next_cookie(self) -> Optional[Dict[str, str]]:
        if self.current_index >= len(self.shuffled_cookies):
            return None
        cookie = self.shuffled_cookies[self.current_index]
        self.current_index += 1
        return cookie

    def reset(self):
        self.shuffled_cookies = self.cookies.copy()
        random.shuffle(self.shuffled_cookies)
        self.current_index = 0

    @staticmethod
    async def generate_images(
        folder_name: str, prompt: str, max_global_retries: int = 5
    ):
        prompt_clean = re.sub(r"[^\x20-\x7E]", "", prompt.strip())
        cookies_file = "storage/cookies/bing/bing.json"
        gen = Bing(cookies_file)
        retries = 0

        while retries < max_global_retries:
            cuki = gen.get_next_cookie()
            if cuki is None:
                logger.warning("Semua cookie sudah dicoba, reset ulang.")
                gen.reset()
                retries += 1
                continue

            luci = AsyncImageGenerator(
                auth_cookie_u=cuki["auth_cookie_u"],
                auth_cookie_srchhpgusr=cuki["auth_cookie_srchhpgusr"],
            )

            try:
                images = await luci.generate(
                    prompt=prompt_clean, num_images=4, max_cycles=4
                )
                if not images:
                    logger.warning(
                        "Tidak ada gambar yang dihasilkan, lanjut cookie berikutnya."
                    )
                    continue

                await luci.save(images, output_dir=folder_name)
                files = [
                    os.path.join(folder_name, f)
                    for f in os.listdir(folder_name)
                    if f.endswith(".jpeg")
                ]

                if files:
                    gen.reset()
                    return folder_name, files

            except Exception as e:
                logger.error(f"Error: {e}")
                continue

        logger.error("Gagal menghasilkan gambar setelah semua retry.")
        return None, None


class AsyncImageGenerator:
    BASE_URL = "https://www.bing.com"

    def __init__(self, auth_cookie_u: str, auth_cookie_srchhpgusr: str):
        self.cookies = {
            "_U": auth_cookie_u,
            "SRCHHPGUSR": auth_cookie_srchhpgusr,
        }
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": f"{self.BASE_URL}/images/create",
        }

    async def _get_ig_value(self, client: httpx.AsyncClient) -> str | None:
        try:
            # Perbaikan: Tambahkan follow_redirects=True untuk melewati HTTP 301
            resp = await client.get(f"{self.BASE_URL}/images/create", follow_redirects=True)
            match = re.search(r'IG:"([A-Z0-9]+)"', resp.text)
            if match:
                return match.group(1)
            logger.warning("IG tidak ditemukan di halaman /images/create.")
        except httpx.RequestError as e:
            logger.error(f"Gagal mengambil IG: {e}")
        return None

    async def generate(
        self, prompt: str, num_images: int, max_cycles: int = 4
    ) -> List[str]:
        async with httpx.AsyncClient(
            headers=self.headers, cookies=self.cookies, timeout=60.0
        ) as client:
            images = []
            start = asyncio.get_event_loop().time()

            ig_value = await self._get_ig_value(client)
            if not ig_value:
                logger.error("Tidak bisa mendapatkan IG, hentikan proses generate.")
                return []

            for cycle in range(1, max_cycles + 1):
                if len(images) >= num_images:
                    break

                redirect_url = await self._submit_prompt(client, prompt)
                if not redirect_url:
                    logger.warning(f"[Cycle {cycle}] Gagal mendapatkan redirect URL.")
                    continue

                result_id = self._extract_result_id(redirect_url)
                results_url = (
                    f"{self.BASE_URL}/images/create/async/results/{result_id}"
                    f"?q={prompt}&IG={ig_value}&IID=images.as"
                )

                async for html in self._wait_for_results(
                    client, results_url, timeout=200
                ):
                    new_images = self._extract_image_urls(html)
                    if new_images:
                        before_count = len(images)
                        images.extend(new_images)
                        images = list(OrderedDict.fromkeys(images))
                        after_count = len(images)
                        logger.info(
                            f"[Cycle {cycle}] Dapat {after_count - before_count} gambar baru."
                        )

                        if len(images) >= num_images:
                            break

            duration = round(asyncio.get_event_loop().time() - start, 2)
            logger.info(f"Generated {len(images)} images in {duration} seconds.")
            return images[:num_images]

    async def _submit_prompt(
        self, client: httpx.AsyncClient, prompt: str
    ) -> Optional[str]:
        for attempt in range(2):
            try:
                resp = await client.post(
                    f"{self.BASE_URL}/images/create?q={prompt}&rt=4&mdl=0&FORM=GENCRE",
                    data={"q": prompt, "qs": "ds"},
                    follow_redirects=True, # Biarkan httpx menangani jika ada redirect internal
                )
                
                # Kasus 1: Bing merespons dengan 200 OK (Struktur Baru)
                if resp.status_code == 200:
                    # Periksa apakah ini halaman blokir/CAPTCHA
                    if "authns" in resp.text or "snrerror" in resp.text:
                        logger.error(f"Attempt {attempt+1}: Cookie kemungkinan diblokir atau butuh CAPTCHA.")
                        return None
                        
                    # Ekstrak ID langsung dari isi teks HTML menggunakan Regex
                    # Bing biasanya menyimpan ID di dalam parameter URL atau payload json internal text
                    id_match = re.search(r'id=([^"& \?]+)', resp.text)
                    if id_match:
                        # Buat format URL tiruan agar fungsi _extract_result_id bawaan Anda tetap bekerja
                        return f"https://bing.com{id_match.group(1)}"
                    
                    # Alternatif ekstraksi jika ID berada di parameter URL akhir setelah follow_redirects
                    if "id=" in str(resp.url):
                        return str(resp.url)

                # Kasus 2: Bing tetap merespons menggunakan skema lama 302/301 (Fallback)
                elif resp.status_code in (301, 302) and resp.headers.get("Location"):
                    return resp.headers["Location"]

                logger.warning(
                    f"Attempt {attempt+1}: Gagal mengenali format respons, status {resp.status_code}"
                )
                await asyncio.sleep(1)
            except httpx.RequestError as e:
                logger.error(f"Submit error: {e}")
                await asyncio.sleep(1)
        return None


    def _extract_result_id(self, location: str) -> str:
        return location.split("id=")[-1].split("&")[0]

    def _extract_image_urls(self, html: str) -> List[str]:
        return [
            "https://tse" + link.split("?w=")[0]
            for link in re.findall(r'src="https://tse([^"]+)"', html)
        ]

    async def save(self, images: List[str], output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        seen_hashes = set()

        async with httpx.AsyncClient(timeout=200.0) as client:
            for idx, url in enumerate(images, 1):
                try:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    img_hash = hashlib.md5(resp.content).hexdigest()

                    if img_hash in seen_hashes:
                        logger.info(f"Duplicate skipped: {url}")
                        continue

                    seen_hashes.add(img_hash)
                    filename = os.path.join(output_dir, f"image_{idx}.jpeg")
                    async with aiofiles.open(filename, "wb") as f:
                        await f.write(resp.content)

                except Exception as e:
                    logger.warning(f"Failed to save {url}: {e}")

    # Melanjutkan fungsi Anda yang terpotong di akhir pesan
    async def _wait_for_results(
        self, client: httpx.AsyncClient, url: str, timeout: int
    ):
        elapsed_time = 0
        interval = 3
        while elapsed_time < timeout:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    yield response.text
                    if "current_status" not in response.text: # Sesuaikan indikator selesai
                        break
            except httpx.RequestError as e:
                logger.error(f"Polling error: {e}")
            
            await asyncio.sleep(interval)
            elapsed_time += interval

