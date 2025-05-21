from django.core.management.base import BaseCommand
from tickets.models import Seat
from matches.models import Match

class Command(BaseCommand):
    help = 'Tạo ghế cho một trận đấu theo sơ đồ định sẵn'

    def add_arguments(self, parser):
        parser.add_argument('match_id', type=int, help='ID của trận đấu cần tạo ghế')

    def handle(self, *args, **kwargs):
        match_id = kwargs['match_id']
        try:
            match = Match.objects.get(pk=match_id)
        except Match.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ Không tìm thấy trận đấu với ID {match_id}"))
            return

        seat_config = {
            'A2': 20,
            'A3': 20,
            'A4': 20,
            'A5': 20,
            'B': 30,
            'C': 30,
            'D': 30,
        }

        created = 0
        for area, quantity in seat_config.items():
            for i in range(1, quantity + 1):
                Seat.objects.create(
                    match=match,
                    seat_number=area,
                )
                created += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Đã tạo {created} ghế cho trận '{match.title}'"))
