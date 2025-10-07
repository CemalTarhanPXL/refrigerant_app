from django.core.management.base import BaseCommand
from ...models import Vessel
import threading
from ...services.vessel_service import withdraw_refrigerant

class Command(BaseCommand):
    help = "Simulate condition when withdrawing refrigerant from a vessel."

    def handle(self, *args, **kwargs):
        Vessel.objects.create(name="Test Vessel", content=50.0)
        self.stdout.write("Simulating condition...")
        self.run_simulation()


    def run_simulation(self):
        barrier = threading.Barrier(2)


        def perform_withdrawal(user_name, amount):
            barrier.wait()
            _, message = withdraw_refrigerant(user_name, 1, amount)
            self.stdout.write(message)

        def user1():
            barrier.wait()
            perform_withdrawal("User 1", 10.0)

        def user2():
            barrier.wait()
            perform_withdrawal("User 2", 10.0)

        t1 = threading.Thread(target=user1)
        t2 = threading.Thread(target=user2)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        vessel = Vessel.objects.get(id=1)
        self.stdout.write(f"Remaining content: {vessel.content} kg")
