# Team decision record — conservative v1.0.0 scope

Team approval reported/confirmed by repository maintainer Dwi Wijonarko on 2026-10-08.

Tanggal: 2026-10-08. Nama file dipertahankan untuk kesinambungan tautan;
statusnya sekarang **catatan keputusan**, bukan usulan yang masih menunggu tim.
Sumber konfirmasi adalah instruksi pengelola Dwi Wijonarko pada tugas ini:
**"Tim sudah setuju semua, tinggal konfirmasi di dokumen."** Tidak ada tanda
tangan individu, izin pihak ketiga, atau provenance historis baru yang diklaim.

## 1. Riwayat dan keputusan yang diadopsi

Dokumen sebelumnya adalah draft berbasis audit untuk pembahasan tim. Draft
mengusulkan rilis konservatif: kode/dokumentasi milik repository, demo sintetis,
hasil demo baru yang berlabel jelas, dan metadata bukti yang ditinjau, dengan
pengecualian seluruh bahan penelitian yang hak distribusinya belum diketahui.
Pengelola kini melaporkan persetujuan tim atas cakupan tersebut. Status
"belum diadopsi tim" pada draft sebelumnya telah digantikan oleh catatan ini.

MIT berlaku untuk kode, dokumentasi, dan demo sintetis milik repository.
Pemegang copyright tetap **PM-BG-AES contributors**. Sembilan nama metadata
beserta urutannya dikonfirmasi sesuai [catatan persetujuan](release_approval.md);
peran kontribusi tertentu tidak ditetapkan.

## 2. Cakupan awal yang disetujui

| Materi                                                                                      | Keputusan                                                                         |
| ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Kode dan dokumentasi milik repository                                                       | Sertakan dengan MIT                                                               |
| DEMO-001..DEMO-011                                                                          | Sertakan sebagai input sintetis, bukan F1..F9                                     |
| Benchmark/figur demo baru                                                                   | Sertakan dengan provenance run baru dan ID `demo-*`                               |
| Notebook publik                                                                             | Salinan `notebooks/public/`, source sel tidak diubah; output/metadata dibersihkan |
| Ringkasan audit dan hash historis yang ditinjau                                             | Sertakan sebagai catatan bukti privat yang dikecualikan                           |
| Triplet original/encrypted/decrypted F1..F9                                                 | Kecualikan seluruhnya dari rilis publik awal                                      |
| Seluruh `results/analysis result/`                                                          | Kecualikan termasuk TXT/MD, log tersalin, notebook tambahan dan UCEF              |
| DOCX manuskrip/laporan, notebook root/raw, artefak hasil/distribusi lama, egg-info terlacak | Kecualikan dari snapshot kandidat                                                 |
| `.git/`, attachment metadata, secrets, konten privat                                        | Tidak dimasukkan dalam paket publik                                               |

Notebook publik bukan salinan full-file dengan checksum identik. Hash notebook
awal pada [inventaris](source_inventory.md) mengidentifikasi original privat,
bukan file publik yang dibersihkan. Lihat
[preservasi dan redaksi](notebook_preservation_and_redaction.md) dan
[review artefak publik](public_artifact_review.csv).

## 3. Jawaban provenance yang tetap berlaku

**Konsistensi artefak terverifikasi; atribusi run historis belum terkonfirmasi.**
Audit sebelumnya mencocokkan Table 3 dengan stdout notebook tersimpan dan
sembilan baris Table 7 dengan laporan TXT/MD. Sembilan pasangan
original–decrypted memiliki hash identik; struktur/segmen permutasi konsisten.
Ini tidak mengautentikasi waktu eksekusi atau membuktikan run historis.

Operator, tanggal, versi notebook/sel/commit, perangkat keras, dependensi,
jumlah pengulangan dan agregasi run asli masih belum terkonfirmasi. Input
Table 3 dan COMNET belum ditemukan. Tool/config UCEF belum tersedia; statistik
full-file F9 berbeda dari sebagian nilai laporan. Shift128 berasal dari
pipeline berbeda; hubungan Figure 7 dan definisi residual masih belum jelas.
Batas ilmiah ini diterima untuk rilis konservatif, bukan dinyatakan terselesaikan.

## 4. Keputusan distribusi bukan izin redistribusi

[Register distribusi](dataset_distribution_review.csv) mencatat keputusan
F1..F9 sebagai `exclude from initial public release; confirmed by maintainer`.
Bukti keputusannya adalah `maintainer-reported team approval for conservative release scope`.
Sumber/pemegang hak tetap belum terdokumentasi. Persetujuan pengecualian bukan
izin afirmatif untuk mendistribusikan original, ciphertext atau decrypted.
Enkripsi tidak menghapus hak cipta atau kerahasiaan. Tidak ada janji
"available upon request" tanpa prosedur yang benar-benar disetujui.

Path pada [identitas dataset](dataset_evidence.csv) sekarang merupakan referensi
historis ke bukti privat yang dikecualikan, bukan input yang tersedia untuk
menjalankan paket publik. Hash dan temuan lama dipertahankan. Pernyataan
"untracked" dari audit awal adalah keadaan saat audit tersebut; sebelum
sanitasi kandidat, materi penelitian kemudian terlacak dalam baseline Git
publik. Menghapus file dari snapshot baru tidak menghapus riwayat paparan.

## 5. Status kandidat dan publikasi

Versi kandidat `1.0.0`, tag yang dimaksud `v1.0.0`, repository
https://github.com/dwi-wijonarko-unej/pm-bg-aes-supplementary.
Run demo yang ditetapkan: `v1.0.0-demo-20261008T020017Z`, dengan bukti hasil
pada `results/runs/v1.0.0-demo-20261008T020017Z/` dan latest copies.

Local candidate prepared; publication performed by maintainer after candidate validation.
Belum ada klaim publikasi, tanggal rilis atau DOI. Kandidat arsip v1.0.0 harus
sesuai snapshot bersih, bukan ZIP lama yang hanya mendapat patch dokumentasi.
Lihat [persetujuan rilis](release_approval.md),
[pernyataan availability](availability_statement_draft.md) dan
[batasan](limitations.md).
