from enum import Enum

class Mission(str, Enum):
    BIRTHDAY = "Birthday"
    GYM = "Gym"
    HOSTEL_SETUP = "Hostel Setup"
    MOVIE_NIGHT = "Movie Night"
    TRAVEL_ESSENTIALS = "Travel Essentials"
    WEEKLY_PREP = "Weekly Prep"
    WORK_FROM_HOME = "Work From Home"

class Category(str, Enum):
    AUTOMOTIVE = "Automotive"
    BEAUTY = "Beauty"
    ELECTRONICS = "Electronics"
    FASHION = "Fashion"
    GROCERIES = "Groceries"
    HEALTH = "Health"
    HOME = "Home"
    OFFICE = "Office"
    OTHER = "Other"
    SPORTS = "Sports"

class Currency(str, Enum):
    INR = "INR"

class InventoryStatus(str, Enum):
    IN_STOCK = "IN_STOCK"
    OUT_OF_STOCK = "OUT_OF_STOCK"
    PREORDER = "PREORDER"

class InteractionType(str, Enum):
    VIEW = "VIEW"
    ADD_TO_CART = "ADD_TO_CART"
    PURCHASE = "PURCHASE"
    SAVE_FOR_LATER = "SAVE_FOR_LATER"

class QuestionType(str, Enum):
    SINGLE_SELECT = "SINGLE_SELECT"
    MULTI_SELECT = "MULTI_SELECT"
    BOOLEAN = "BOOLEAN"
    NUMBER = "NUMBER"

class UrgencyLevel(str, Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    IMMEDIATE = "IMMEDIATE"

class IntentStatus(str, Enum):
    SUPPORTED = "SUPPORTED"
    UNSUPPORTED = "UNSUPPORTED"
    AMBIGUOUS = "AMBIGUOUS"

class QuestionID(str, Enum):
    ASK_BUDGET = "ASK_BUDGET"
    ASK_BRAND_PREFERENCE = "ASK_BRAND_PREFERENCE"
    ASK_MISSING_CATEGORY = "ASK_MISSING_CATEGORY"
    ASK_DELIVERY_TIME = "ASK_DELIVERY_TIME"
    ASK_USAGE_CONTEXT = "ASK_USAGE_CONTEXT"
    ASK_COOKING = "ASK_COOKING"
    ASK_ROOM_TYPE = "ASK_ROOM_TYPE"
    ASK_TRIP_DURATION = "ASK_TRIP_DURATION"
    ASK_WORK_MODE = "ASK_WORK_MODE"
    ASK_GYM_GOAL = "ASK_GYM_GOAL"
    ASK_PRIORITY = "ASK_PRIORITY"
