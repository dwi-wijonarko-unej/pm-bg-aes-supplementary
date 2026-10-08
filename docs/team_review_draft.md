# Draft jawaban provenance dan distribusi dataset untuk tim

Tanggal penyusunan: 2026-10-08.
Status: **usulan berbasis audit repository, untuk dibahas oleh tim; bukan
persetujuan pelaksana eksperimen atau pemegang hak**.

Pengelola repository meminta penyusunan jawaban dan perubahan dokumentasi
untuk pembahasan tim. Mandat tersebut mengizinkan penyusunan draft, bukan
pembuktian asal eksperimen atau pemberian izin atas materi pihak ketiga.
Lisensi MIT sudah dikonfirmasi pengelola untuk materi milik repository.

Sumber bukti: [laporan audit](evidence_audit.md),
[identitas dataset](dataset_evidence.csv),
[pemetaan naskah–artefak](manuscript_artifact_mapping.csv), dan
[lembar keputusan distribusi](dataset_distribution_review.csv).
Path artefak dalam dokumen ini relatif terhadap root repository.

## 1. Jawaban provenance yang saya rekomendasikan

> Repository memuat implementasi yang diarsipkan dari notebook yang tersedia,
> bahan pendukung eksperimen, dan hasil demonstrasi baru yang dipisahkan secara
> eksplisit. Angka Table 3 cocok dengan output dekripsi tersimpan pada notebook
> `ori` sel 1. Seluruh sembilan baris Table 7 cocok dengan laporan benchmark
> TXT/MD yang disertakan. File berlabel F1–F9, ciphertext, dan hasil decrypted
> tersedia lokal; sembilan pasangan original–decrypted identik, dan ukuran,
> header, serta segmen permutasi konsisten dengan implementasi PM-BG.
>
> Dengan demikian, keterlacakan numerik dan konsistensi artefak telah
> diperiksa. Bukti tersebut mendukung penggunaan file sebagai **bahan
> pendukung hasil yang dilaporkan**, tetapi belum mengautentikasi run historis
> yang menghasilkan waktu eksekusi. Identitas pelaksana, tanggal run,
> notebook/sel/commit yang dijalankan, perangkat keras, versi dependensi,
> jumlah pengulangan, dan aturan agregasi angka belum terkonfirmasi.
> Hasil demo baru bukan pengganti bukti eksperimen asli.

**Status yang dipakai:** konsistensi artefak terverifikasi; atribusi run asli
belum terkonfirmasi. Jangan menyederhanakannya menjadi "provenance tidak ada"
atau "seluruh hasil paper telah direproduksi".

| Item | Jawaban berdasarkan bukti | Batas yang harus tetap dicatat |
|---|---|---|
| Implementasi PM-BG | Sel 1 `PM_BG_+_AES_(works)_ori.ipynb` dipilih sebagai referensi arsip; source sel tersebut sama dengan sel 1 workshop; salinan `notebooks/original/` identik dengan root | Pemilihan referensi arsip bukan konfirmasi versi seluruh eksperimen |
| Table 3 | Output tersimpan cocok: 0.0070 s, 14.27 MiB/s, 1125.57 KB, 99.9%, 104300 → 104267 byte | File input `FileAttachment.pdf_encrypted` belum ditemukan; belum ada rerun benchmark asli |
| Table 7 | Sembilan baris cocok dengan `results/analysis result/2. File TXT - Paper PM-BG + AES_ori.txt`; salinan MD identik | Laporan tersimpan tidak membuktikan environment, jumlah run, atau proses agregasi |
| F1–F9 | Ukuran/hash dicatat; 9/9 original–decrypted sama; struktur/segmen utama ciphertext konsisten | Identitasnya sebagai input run historis perlu konfirmasi pelaksana; integritas tidak membuktikan hak distribusi |
| UCEF | Laporan v1.0 dan v3.0 tersedia; skor 60.00/100 mempunyai bukti laporan | Tool/config/input-run hash dan ekspor mandiri belum tersedia; sebagian statistik F9 berbeda dari hitungan full-file |
| Shift128 | Implementasi ±128 mod 256 ditemukan pada notebook graph/unimodular/AES seluruh payload | Bukan pipeline PM-BG/AES-tail; kaitan dengan Figure 7 dan definisi residual belum jelas |
| Hasil demo | DEMO-001..011, konfigurasi, pengukuran berulang, dan lingkungan run tersedia | Merupakan eksekusi lokal baru, bukan hasil run historis penelitian |

Nama file, label `ori`, tanggal pada judul laporan, execution count, atau waktu
modifikasi file tidak cukup untuk menetapkan tanggal eksperimen dan pelaksana.
Tidak ada data tersebut yang ditafsirkan sebagai persetujuan tertulis.

## 2. Jawaban izin distribusi yang saya rekomendasikan

> Materi milik repository berupa kode, dokumentasi, dan data demo sintetis
> menggunakan MIT. Untuk F1–F9, sumber perolehan, pemilik hak, syarat lisensi,
> dan izin distribusi belum terdokumentasi. Karena itu, saya mengusulkan agar
> file asli, ciphertext, dan hasil decrypted F1–F9 **tidak dimasukkan ke rilis
> publik awal**. Seluruh `results/analysis result/` juga diusulkan dikecualikan
> sementara, termasuk laporan, log tersalin, dan notebook tambahan, sampai
> review per artefak selesai.
>
> Keputusan ini adalah cakupan rilis yang direkomendasikan, bukan klaim bahwa
> pemegang hak melarang distribusi. Identitas file, ukuran, checksum, dan
> ringkasan keterlacakan dapat dipertimbangkan untuk publikasi setelah review
> privasi dan persetujuan cakupan. Jika tim kemudian menyediakan bukti hak,
> hanya file yang disetujui secara spesifik yang ditambahkan dengan lisensi
> atau ketentuan distribusi yang sesuai.

Enkripsi tidak menghilangkan kewajiban hak cipta atau kerahasiaan. File
berformat TXT/JPG/MP4 pun tidak otomatis bebas distribusi; EXE/MSI/ZIP tidak
otomatis dilarang hanya karena formatnya. Semua F1–F9 diperlakukan sama sampai
sumber dan haknya diketahui. EXE/MSI tidak perlu dijalankan untuk review ini.

### Usulan cakupan rilis awal (belum diadopsi tim)

| Materi | Rekomendasi | Syarat sebelum benar-benar dipublikasikan |
|---|---|---|
| Kode dan dokumentasi milik repository | Sertakan, MIT | Review hak kode/notebook, privacy, dan persetujuan rilis |
| DEMO-001..011 | Sertakan, MIT | Verifikasi manifest dan pertahankan label sintetis |
| Hasil benchmark/figur demo baru | Sertakan, label demo | Periksa provenance lokal dan bebas informasi privat; jangan relabel menjadi figur asli paper |
| Metadata F1–F9 dan ringkasan audit | Sertakan hanya yang lolos review | Nilai apakah nama/hash/ukuran/ringkasan boleh diketahui publik |
| File original/encrypted/decrypted F1–F9 | Kecualikan sementara | Bukti kepemilikan atau lisensi pihak ketiga dan izin per file |
| Isi `results/analysis result/`, termasuk TXT/MD, notebook tambahan, dan laporan UCEF | Kecualikan sementara sebagai satu folder | Perizinan per artefak dan review password/data privat; bila nanti diizinkan, gunakan daftar inklusi eksplisit |
| Manuskrip DOCX, attachment metadata, secrets | Jangan sertakan dalam rilis awal | Naskah hanya dapat dipertimbangkan terpisah dengan izin yang relevan; secrets tidak dipublikasikan |

**Belum diterapkan pada builder.** `scripts/build_release.py` masih menelusuri
seluruh `results/` tanpa per-file rights gate. Dokumen ini tidak mengubah
perilaku kode dan tidak membuat archive/publication baru. Rekomendasi perlu
diadopsi tim dan diterapkan sebagai filter/allowlist sebelum membangun paket.
Archive lokal lama bukan bukti bahwa semua file workspace siap dirilis.

## 3. Lembar keputusan F1–F9

`docs/dataset_distribution_review.csv` berisi sembilan baris yang siap dibahas:

- Sumber/pemilik hak: belum terdokumentasi.
- Bukti izin: belum tercatat; tidak disimpulkan dari ekstensi/nama/hash.
- Tindakan yang diusulkan: kecualikan triplet dari rilis publik awal.
- Keputusan tim: belum ditetapkan.

Untuk setiap ID, tim dapat memilih:

1. **Publik:** catat pemilik/sumber, lisensi/ketentuan, file yang disetujui,
   bukti persetujuan, penanggung jawab, dan tanggal keputusan. Original,
   encrypted, dan decrypted tidak dianggap otomatis satu izin bersama.
2. **Terbatas:** jelaskan mekanisme akses yang memang disepakati serta
   penanggung jawabnya. Jangan menjanjikan "available upon request" sebelum
   prosedur dan kontak tersedia.
3. **Tidak didistribusikan:** dokumentasikan keputusan/alasannya tanpa
   menyatakan file hilang atau hasil telah direproduksi.
4. **Belum diputuskan:** pertahankan pengecualian publik dan status draft.

Saya tidak mengisi nama penanggung jawab, pemilik hak, atau tanggal persetujuan
atas nama tim. Keberadaan file lokal tidak membuktikan bahwa file boleh
diedarkan internal tanpa batas; review dilakukan hanya melalui pihak yang
berwenang menerima bahan tersebut.

## 4. Pernyataan lokal yang bisa dipakai sekarang

> Kode, dokumentasi, dan data demo sintetis milik repository berlisensi MIT.
> Pemeriksaan lokal menemukan padanan numerik Table 3 pada output notebook
> tersimpan dan seluruh baris Table 7 pada laporan teks. F1–F9 tersedia lokal
> dan integritas sembilan pasangan original–decrypted terverifikasi.
> Atribusi run historis dan izin distribusi per file belum terdokumentasi.
> Untuk pembahasan tim, rilis awal diusulkan berfokus pada kode, data demo,
> hasil demo, dan metadata yang telah lolos review; file penelitian dan
> laporan pendukung dikecualikan sampai izin serta cakupan rilis ditetapkan.
> Pernyataan ini tidak menyatakan publikasi telah dilakukan atau seluruh
> hasil paper telah direproduksi.

Draft availability berbahasa Inggris ada di
[availability statement](availability_statement_draft.md). Jangan isi URL/DOI
fiktif atau mengganti bentuk "diusulkan" menjadi "telah disetujui" sebelum
keputusan yang relevan tercatat.

## 5. Pesan pembahasan siap-kirim

> Rekan-rekan, berdasarkan pemeriksaan repository saya mengusulkan kita
> mengakui dua hal secara terpisah: (1) kecocokan angka dan konsistensi
> artefak sudah diperiksa, tetapi atribusi run asli belum lengkap; (2) MIT
> berlaku untuk materi milik repository, tetapi hak distribusi F1–F9 dan
> laporan pendukung belum terdokumentasi.
>
> Untuk rilis awal, usulannya adalah kode, DEMO-001..011, hasil demo berlabel
> jelas, dan metadata yang lolos review. F1–F9 beserta ciphertext/decrypted
> dan folder laporan penelitian tidak dimasukkan dahulu. Mohon tim menilai
> atau mengoreksi draft ini, mengonfirmasi pelaksana/versi/lingkungan/run yang
> mendasari Tables 3/7, dan menetapkan status distribusi tiap file dengan
> bukti haknya. Jika informasi historis tidak tersedia, cukup dokumentasikan
> keterbatasannya; tidak perlu membuat ulang angka lalu menyebutnya run asli.
>
> Usulan ini belum menjadi persetujuan publikasi. Setelah keputusan tim
> tercatat, dokumentasi, daftar inklusi, dan paket rilis dapat difinalkan.
