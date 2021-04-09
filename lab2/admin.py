import datetime
import logging
import redis
from threading import Thread

logging.basicConfig(filename="events.log", level=logging.INFO)

delimiter = 46 * "-"
delimiter_half = 20 * "-"

class EventListener(Thread):
    def __init__(self, connection):
        Thread.__init__(self)
        self.connection = connection

    def is_message(item):
        return item['type'] == 'message'

    def run(self):
        pubsub = self.connection.pubsub()
        pubsub.subscribe(["users", "spam"])
        for item in pubsub.listen():
            if self.is_message(item):
                logging.info("Event detached: %s. Detached at %s\n" % (item['data'], datetime.datetime.now()))


def admin_menu():
    print(delimiter_half, "MENU", delimiter_half)
    print("1. Online users")
    print("2. Top senders")
    print("3. Top spammers")
    print("4. Exit")
    print(delimiter)


def online_users(connection):
    online_users = connection.smembers("online:")
    print("Users online:")
    for user in online_users:
        print(user)


def top_senders(connection):
    top_senders_count = int(input("Enter count of top senders: "))
    senders = connection.zrange("sent:", 0, top_senders_count - 1, desc=True, withscores=True)
    print("Top %s senders" % top_senders_count)
    for index, sender in enumerate(senders):
        print(index + 1, ". ", sender[0], " - ", int(sender[1]), "message(s)")


def top_spamers(connection):
    top_spamers_count = int(input("Enter count of top spamers: "))
    spamers = connection.zrange("spam:", 0, top_spamers_count - 1, desc=True, withscores=True)
    print("Top %s spamers" % top_spamers_count)
    for index, spamer in enumerate(spamers):
        print(index + 1, ". ", spamer[0], " - ", int(spamer[1]), " spammed message(s)")


def main():
    connection = redis.Redis(charset="utf-8", decode_responses=True)
    listener = EventListener(connection)
    listener.setDaemon(True)
    listener.start()

    while True:
        admin_menu()
        choice = int(input("Enter your choice [1-4]: "))

        if choice == 1:
            online_users(connection)

        elif choice == 2:
            top_senders(connection)

        elif choice == 3:
            top_spamers(connection)

        elif choice == 4:
            print("Exiting...")
            break
        else:
            print("Wrong option selection. Enter any key to try again..")


if __name__ == '__main__':
    main()