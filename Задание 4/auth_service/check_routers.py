try:
    print("1. Checking auth router...")
    from app.api.endpoints.auth import router as auth_router
    print(f"Auth router: prefix={auth_router.prefix}, tags={auth_router.tags}")
    
    print("2. Checking user router...")
    from app.api.endpoints.user import router as user_router
    print(f"User router: prefix={user_router.prefix}, tags={user_router.tags}")
    
    print("3. Checking if routers have endpoints...")
    print(f"   Auth routes: {len(auth_router.routes)}")
    print(f"   User routes: {len(user_router.routes)}")
    
    print("\nAll routers are properly configured!")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()