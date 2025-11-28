async def handler(_event, _context):
    from app.core.controllers.activity_controllers import add_new_activities_to_db

    try:
        activities = await add_new_activities_to_db()
    except Exception as e:
        print("Failed to upload activities:", e)
        activities = []

    return {
        "statusCode": 200,
        "body": f"Uploaded {len(activities)} activities"
    }
