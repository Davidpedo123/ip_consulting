import pytest
from src import namespace
from fastapi import HTTPException
from src.user_case.get_ip_info_use_case import GetIPInfoUseCase

def test_validate_ip_valid_ipv4():
    # Should not raise any exception
    GetIPInfoUseCase.validate_ip("8.8.8.8")

def test_validate_ip_valid_ipv6():
    # Should not raise any exception
    GetIPInfoUseCase.validate_ip("2001:4860:4860::8888")

def test_validate_ip_invalid_format():
    with pytest.raises(HTTPException) as excinfo:
        GetIPInfoUseCase.validate_ip("invalid-ip")
    assert excinfo.value.status_code == 400
    assert "Invalid IP address format" in excinfo.value.detail

def test_check_invalid_ip_none_data():
    with pytest.raises(HTTPException) as excinfo:
        GetIPInfoUseCase.check_invalid_ip(None)
    assert excinfo.value.status_code == 404

def test_check_invalid_ip_invalid_value():
    data = {"ip": "INVALID IP ADDRESS", "city": "-"}
    with pytest.raises(HTTPException) as excinfo:
        GetIPInfoUseCase.check_invalid_ip(data)
    assert excinfo.value.status_code == 400
    assert "Invalid IP address value in the record" in excinfo.value.detail

def test_check_invalid_ip_valid_data():
    data = {"ip": "8.8.8.8", "city": "Mountain View"}
    result = GetIPInfoUseCase.check_invalid_ip(data)
    assert result == data
