def test_public_api_exports():
    import interservice as pkg

    assert hasattr(pkg, "verify_internal_token")
    assert hasattr(pkg, "BaseHTTPService")
    assert hasattr(pkg, "Services")
    assert hasattr(pkg, "get_service_client")


