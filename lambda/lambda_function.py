import json
import boto3
import uuid
from datetime import datetime

sagemaker = boto3.client('sagemaker-runtime')
dynamodb = boto3.resource('dynamodb')

# GANTI 2 KONFIGURASI DI BAWAH INI SESUAI PUNYA KELOMPOK KALIAN
ENDPOINT_NAME = 'cm-loan-endpoint-namakelompok'
TABLE_NAME = 'CMLoan-Riwayat-NamaKelompok'

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        nama = body.get('nama', 'Anonim')
        umur = int(body.get('umur', 25))
        pekerjaan = int(body.get('pekerjaan', 2)) # 1=Lepas, 2=Swasta, 3=PNS/BUMN, 4=Pengusaha
        gaji = float(body.get('gaji', 5))         # Dalam Juta Rupiah
        lama_kerja = int(body.get('lama_kerja', 1))
        pinjaman = float(body.get('pinjaman', 10)) # Dalam Juta Rupiah
        
        # 1. Susun fitur CSV sesuai urutan training: umur, pekerjaan, gaji, lama_kerja, pinjaman
        payload = f"{umur},{pekerjaan},{gaji},{lama_kerja},{pinjaman}"
        
        # 2. Panggil SageMaker Endpoint
        response = sagemaker.invoke_endpoint(
            EndpointName=ENDPOINT_NAME,
            ContentType='text/csv',
            Body=payload
        )
        probabilitas = float(response['Body'].read().decode('utf-8').strip())
        persen_risiko = round(probabilitas * 100, 1)
        
        # 3. Tentukan Keputusan (Threshold 50%)
        if probabilitas >= 0.5:
            status = "HIGH RISK (DITOLAK)"
            pesan = f"Halo {nama}, pengajuan Rp {pinjaman} Juta dinilai BERISIKO TINGGI ({persen_risiko}%). Rasio pinjaman tidak seimbang dengan gaji Rp {gaji} Juta/bulan."
        else:
            status = "LOW RISK (DISETUJUI)"
            pesan = f"Selamat {nama}! Pengajuan Rp {pinjaman} Juta dinilai AMAN / RELIABLE (Risiko hanya {persen_risiko}%)."

        # 4. Simpan Riwayat ke DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        table.put_item(Item={
            'id_pengajuan': str(uuid.uuid4())[:8],
            'waktu': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'nama': nama,
            'umur': umur,
            'gaji_juta': str(gaji),
            'pinjaman_juta': str(pinjaman),
            'skor_risiko': f"{persen_risiko}%",
            'status': status
        })

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'status': status,
                'skor': persen_risiko,
                'pesan': pesan
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }
