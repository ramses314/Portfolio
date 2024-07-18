from django.core.management.base import BaseCommand
from django.utils.timezone import now

from applications.events.models import Category, Event, Prize, Ticket


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_electronics: Category = Category.objects.create(title='Electronics')
        ps_5: Event = Event.objects.create(
            title='Imagine ps5',
            slug='imagine-ps5',
            content='_blank',
            expired=str(now()),
            ticket_quantity=1500,
            category=category_electronics,
            link='https://www.youtube.com/watch?v=jfKfPfyJRdk',
        )
        Prize.objects.create(title='ps5', content='3 winners', event=ps_5)
        for number in range(1, 1501):
            Ticket.objects.create(
                event=ps_5,
                number=number,
                price=7.50,
            )

        tv_60: Event = Event.objects.create(
            title='Imagine TV screen 60”',
            slug='imagine-tv-screen-60',
            content='_blank',
            expired=str(now()),
            ticket_quantity=1500,
            category=category_electronics,
            link='https://www.youtube.com/watch?v=jfKfPfyJRdk',
        )
        Prize.objects.create(title='Imagine TV screen 60”', content='3 winners', event=tv_60)
        for number in range(1, 1500):
            Ticket.objects.create(
                event=tv_60,
                number=number,
                price=10,
            )

        beats: Event = Event.objects.create(
            title='Imagine Beats Headphones',
            slug='beats-headphones',
            content='_blank',
            expired=str(now()),
            ticket_quantity=2500,
            category=category_electronics,
            link='https://www.youtube.com/watch?v=jfKfPfyJRdk',
        )
        Prize.objects.create(title='Beats Headphones', content='5 winners', event=beats)
        for number in range(1, 2501):
            Ticket.objects.create(
                event=beats,
                number=number,
                price=1.5,
            )
        self.stdout.write(self.style.SUCCESS('Electronics finish'))
        category_travel: Category = Category.objects.create(title='Travel')
        alaska: Event = Event.objects.create(
            title='Imagine Alaska Cruise',
            slug='alaska',
            content='_blank',
            expired=str(now()),
            ticket_quantity=1200,
            category=category_travel,
            link='https://www.youtube.com/watch?v=jfKfPfyJRdk',
        )
        Prize.objects.create(title='Alaska Cruise', content='3 winners', event=alaska)
        for number in range(1, 1201):
            Ticket.objects.create(
                event=alaska,
                number=number,
                price=22.50,
            )

        bahamas: Event = Event.objects.create(
            title='Imagine Bahamas Cruise',
            slug='bahamas',
            content='_blank',
            expired=str(now()),
            ticket_quantity=2000,
            category=category_travel,
            link='https://www.youtube.com/watch?v=jfKfPfyJRdk',
        )
        Prize.objects.create(title='Bahamas Cruise', content='5 winners', event=bahamas)
        for number in range(1, 2001):
            Ticket.objects.create(
                event=bahamas,
                number=number,
                price=15,
            )

        cozumel: Event = Event.objects.create(
            title='Imagine Cozumel Cruise',
            slug='cozumel',
            content='_blank',
            expired=str(now()),
            ticket_quantity=4000,
            category=category_travel,
            link='https://www.youtube.com/watch?v=jfKfPfyJRdk',
        )
        Prize.objects.create(title='Cozumel Cruise', content='10 winners', event=cozumel)
        for number in range(1, 4001):
            Ticket.objects.create(
                event=cozumel,
                number=number,
                price=11.50,
            )
        self.stdout.write(self.style.SUCCESS('Travel finish'))
        category_experiences: Category = Category.objects.create(title='Experiences')
        vip: Event = Event.objects.create(
            title='Imagine VIP experience',
            slug='vip',
            content='_blank',
            expired=str(now()),
            ticket_quantity=1000,
            category=category_experiences,
            link='https://www.youtube.com/watch?v=jfKfPfyJRdk',
        )
        Prize.objects.create(title='VIP experience', content='1 winner (for 2 people)', event=vip)
        for number in range(1, 1001):
            Ticket.objects.create(
                event=vip,
                number=number,
                price=25,
            )

        platinum: Event = Event.objects.create(
            title='Imagine Platinum experience',
            slug='platinum',
            content='_blank',
            expired=str(now()),
            ticket_quantity=2000,
            category=category_experiences,
            link='https://www.youtube.com/watch?v=jfKfPfyJRdk',
        )
        Prize.objects.create(title='Platinum experience', content='2 winners (for 2 people)', event=platinum)
        for number in range(1, 2001):
            Ticket.objects.create(
                event=platinum,
                number=number,
                price=19,
            )

        plus: Event = Event.objects.create(
            title='Imagine Plus experience',
            slug='plus',
            content='_blank',
            expired=str(now()),
            ticket_quantity=3000,
            category=category_experiences,
            link='https://www.youtube.com/watch?v=jfKfPfyJRdk',
        )
        Prize.objects.create(title='Plus experience', content='3 winners', event=plus)
        for number in range(1, 3001):
            Ticket.objects.create(
                event=plus,
                number=number,
                price=12.50,
            )
        self.stdout.write(self.style.SUCCESS('experiences finish'))
        category_vehicles: Category = Category.objects.create(title='Vehicles')
        t8: Event = Event.objects.create(
            title='Imagine Toyota Hilux 2.8L',
            slug='t8',
            content='_blank',
            expired=str(now()),
            ticket_quantity=1850,
            category=category_vehicles,
            link='https://www.youtube.com/watch?v=jfKfPfyJRdk',
        )
        Prize.objects.create(title='Toyota Hilux 2.8L', content='1 winner', event=t8)
        for number in range(1, 1851):
            Ticket.objects.create(
                event=t8,
                number=number,
                price=50,
            )

        t4: Event = Event.objects.create(
            title='Imagine Toyota Hilux 2.4L',
            slug='t4',
            content='_blank',
            expired=str(now()),
            ticket_quantity=3700,
            category=category_vehicles,
            link='https://www.youtube.com/watch?v=jfKfPfyJRdk',
        )
        Prize.objects.create(title='Toyota Hilux 2.4L', content='2 winners', event=t4)
        for number in range(1, 3701):
            Ticket.objects.create(
                event=t4,
                number=number,
                price=35,
            )
        self.stdout.write(self.style.SUCCESS('Vehicles finish'))
        category_money: Category = Category.objects.create(title='Money')
        money: Event = Event.objects.create(
            title='Imagine Money',
            slug='money',
            content='_blank',
            expired=str(now()),
            ticket_quantity=13500,
            category=category_money,
            link='https://www.youtube.com/watch?v=jfKfPfyJRdk',
        )
        Prize.objects.create(title='$2,500 USD each month over 10 years', content='1 winner', event=money)
        Prize.objects.create(title='$1,000 USD each month over 10 years', content='3 winners', event=money)
        Prize.objects.create(title='$500 USD each month over 10 years', content='5 winners', event=money)
        for number in range(1, 13501):
            Ticket.objects.create(
                event=money,
                number=number,
                price=99,
            )
        self.stdout.write(self.style.SUCCESS('Money finish'))
