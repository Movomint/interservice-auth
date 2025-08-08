def test_public_api_exports():
    import interservice as pkg

    assert hasattr(pkg, "verify_internal_token")
    assert hasattr(pkg, "register_service")
    assert hasattr(pkg, "BaseHTTPService")
    assert hasattr(pkg, "Services")


