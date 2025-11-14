#https://www.cs.toronto.edu/~guerzhoy/180/proj/gamify/gamify.pdf
#October 2, 2025
cur_hedons = 0
cur_health = 0
cur_time = 0
last_activity = None
last_exhausting_activity_end_time = -120
last_star_activity = None
last_star_time = -1
stars_given = []
bored_with_stars = False
continuous_running_time = 0


def get_cur_hedons(): #get_cur_hedons displays the current hedons
    return cur_hedons


def get_cur_health(): #get_cur_health displays the current health
    return cur_health


def offer_star(activity): #offer_star processes if the user can take a star or if they will become bored
    global last_star_activity, last_star_time, stars_given, bored_with_stars, cur_time

    if bored_with_stars:
        return

    last_star_activity = activity
    last_star_time = cur_time
    stars_given.append(cur_time)

    keep_stars = []
    for t in stars_given:
        if cur_time - t < 120:
            keep_stars.append(t)

    stars_given = keep_stars

    if len(stars_given) >= 3:
        bored_with_stars = True


def perform_activity(activity, duration): #perform_activity updates the amount of hedons and health the user has after performing an activity for a specified duration while taking into account star usage
    global cur_hedons, cur_health, cur_time, last_activity, last_exhausting_activity_end_time
    global last_star_activity, last_star_time, continuous_running_time

    if activity != "running" and activity != "textbooks" and activity !="resting":
        return

    cur_hedons += hedons_gain(activity, duration)
    cur_health += health_gain(activity, duration)

    cur_time += duration
    last_activity = activity

    if activity == "running" or activity == "textbooks":
        last_exhausting_activity_end_time = cur_time

    if activity == "running":
        continuous_running_time += duration
    else:
        continuous_running_time = 0

    last_star_activity = None
    last_star_time = -1


def star_can_be_taken(activity): #star_can_be_taken sees whether or not the user has already consumed too many stars and is bored, and rejects the stars, or if they still have capacity to use stars
    if bored_with_stars:
        return False
    if last_star_activity == activity and last_star_time == cur_time:
        return True
    return False


def most_fun_activity_minute(): #most_fun_activity_minute determines which activity is giving the user the most hedons and designates that as the most fun activity
    scores = {"running": hedons_gain("running", 1),"textbooks": hedons_gain("textbooks", 1),"resting": hedons_gain("resting", 1)}
    max_hedons = max(scores.values())
    if scores["running"] == max_hedons:
        return "running"
    if scores["textbooks"] == max_hedons:
        return "textbooks"
    return "resting"

def initialize(): #the initialize function simply initializes all variables we will be using during this code
    global cur_hedons, cur_health, cur_time, last_activity, last_exhausting_activity_end_time
    global last_star_activity, last_star_time, stars_given, bored_with_stars, continuous_running_time

    cur_hedons = 0
    cur_health = 0
    cur_time = 0
    last_activity = None
    last_exhausting_activity_end_time = -120
    last_star_activity = None
    last_star_time = -1
    stars_given = []
    bored_with_stars = False
    continuous_running_time = 0

def is_tired(): #is_tired decides whether or not the user has exceeded the 120 minute limit for running and textbooks to determine whether or not they are tired
    global cur_time, last_exhausting_activity_end_time
    if cur_time - last_exhausting_activity_end_time < 120:
        return True
    else:
        return False


def hedons_gain(activity, duration): #hedons_gain shows how many hedons are gained per activity, including the restrictions on bonus time and hedon gain
    if activity != "running" and activity != "textbooks" and activity != "resting":
        return 0

    hedons = 0
    bonus = 0

    if star_can_be_taken(activity):
        bonus_duration = min(10, duration)
        bonus = bonus_duration * 3

    if is_tired() and (activity == "running" or activity == "textbooks"):
        hedons += duration * -2
    else:
        if activity == "running":
            run10 = min(10, duration)
            hedons += run10 * 2
            hedons += (duration - run10) * -2
        elif activity == "textbooks":
            book20 = min(20, duration)
            hedons += book20
            hedons += (duration - book20) * -1
        else:
            hedons += 0

    return hedons + bonus


def health_gain(activity, duration): #health_gain shows how much health is gained per activity. This includes the restriction that running less than 180 minutes gives 3 healths
    global continuous_running_time
    health = 0
    if activity == "running":
        mins_at_3_rate = min(duration, max(0, 180 - continuous_running_time))
        mins_at_1_rate = duration - mins_at_3_rate
        health = (mins_at_3_rate * 3) + (mins_at_1_rate * 1)
    elif activity == "textbooks":
        health = duration * 2
    else:
        health = 0
    return health


if __name__ == "__main__":
    initialize()
    perform_activity("running", 30)
    print(get_cur_hedons()) # -20 = 10 * 2 + 20 * (-2)
    print(get_cur_health()) # 90 = 30 * 3
    print(most_fun_activity_minute()) # resting
    perform_activity("resting", 30)
    offer_star("running")
    print(most_fun_activity_minute()) # running
    perform_activity("textbooks", 30)
    print(get_cur_health()) # 150 = 90 + 30*2