from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get('/health').json()['data_status']=='DEMO'
def test_stock():
    r=client.get('/api/v1/stocks/RELIANCE'); assert r.status_code==200; assert r.json()['data_status']=='DEMO'
def test_scanner(): assert client.get('/api/v1/scanner').status_code==200
