class Options:
    # TODO: List of URLs
    USE_OPTIONS = True

    '''
    Operating System
    '''
    OSX = True
    WINDOWS = False
    LINUX = False


    '''
    Searching Options
    '''
    LOCATION = 'MacLeod Provincial Park'#'Awenda Provincial Park'
    CAMPGROUND = 'Campground A'#'Snake Campground'
    TIME_TO_RETRY = 10 # seconds
    PRIORITIZE = 'quality' # 'privacy'
    START_DATE = '2021-07-02' # Format is yyyy-MM-dd
    END_DATE = '2021-07-04' # Format is yyyy-MM-dd
    NUMBER_OF_NIGHTS = int((END_DATE.split('-')[-1])) - int((START_DATE.split('-')[-1]))
    EQUIPMENT = 1 # This means number of structures (tent, gazebo, etc.)
    '''
    Notification Options
    '''
    NOTIFY_BY_EMAIL = True
    EMAIL = 'test@example.com'
    APP_PASS = 'use-an-app-password'
