from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from ministry.models import Article, Event, Message, Scripture, SiteSettings, Testimony, TodaysWord


class Command(BaseCommand):
    help = "Load sample ministry content for first launch."

    def handle(self, *args, **options):
        SiteSettings.get()
        today = timezone.localdate()

        TodaysWord.objects.update_or_create(
            date=today,
            defaults={
                "title": "Today's Word",
                "thought": (
                    "God has not called you to live without purpose. The gifts He placed "
                    "within you are part of His design for your life."
                ),
                "verse_text": "Commit your works to the LORD, and your plans will be established.",
                "verse_reference": "Proverbs 16:3",
                "encouragement": (
                    "You do not have to manufacture a calling. You are invited to walk with "
                    "the One who already authored it. Offer Him the work of your hands today, "
                    "and trust Him to establish what you cannot yet see."
                ),
                "prayer": (
                    "Father, I commit my work, my gifts, and my future to You. Establish "
                    "Your purpose in me, and make me a faithful witness of Jesus Christ. Amen."
                ),
                "is_published": True,
            },
        )

        scriptures = [
            (
                "calling",
                "Before I formed you in the womb I knew you, and before you were born I consecrated you.",
                "Jeremiah 1:5",
                True,
            ),
            (
                "purpose",
                "For we are His workmanship, created in Christ Jesus for good works.",
                "Ephesians 2:10",
                False,
            ),
            (
                "witness",
                "You will receive power when the Holy Spirit has come upon you, and you will be My witnesses.",
                "Acts 1:8",
                False,
            ),
            (
                "generation",
                "One generation shall commend Your works to another, and shall declare Your mighty acts.",
                "Psalm 145:4",
                False,
            ),
            (
                "faith",
                "Now faith is the assurance of things hoped for, the conviction of things not seen.",
                "Hebrews 11:1",
                False,
            ),
            (
                "courage",
                "Have I not commanded you? Be strong and courageous. Do not be frightened.",
                "Joshua 1:9",
                False,
            ),
        ]
        for i, (theme, text, ref, featured) in enumerate(scriptures):
            Scripture.objects.update_or_create(
                reference=ref,
                defaults={
                    "verse_text": text,
                    "theme": theme,
                    "is_featured": featured,
                    "order": i,
                },
            )

        articles = [
            {
                "title": "You Were Formed With Purpose",
                "category": "purpose",
                "excerpt": "God does not waste a life. The gifts within you are an invitation to walk with Him.",
                "body": (
                    "Purpose is not a slogan. It is the quiet conviction that your life belongs to God, "
                    "and that He is able to use ordinary obedience in extraordinary ways.\n\n"
                    "David's ministry exists to help people discover that they are not accidents of history, "
                    "but sons and daughters called to know Christ and make Christ known.\n\n"
                    "Begin where you are. Offer God the work of your hands. Trust Him with the rest."
                ),
                "image_fallback": "portrait-thoughtful.jpg",
                "is_featured": True,
            },
            {
                "title": "This Generation Is Not Waiting",
                "category": "youth",
                "excerpt": "Young people are not merely the church of tomorrow. God can use them today.",
                "body": (
                    "A generation is rising that is hungry for truth, identity, and a faith that can stand "
                    "in the real world.\n\n"
                    "Mentorship is not optional. Discipleship is not a program. It is a life poured out so "
                    "that another life can walk with Jesus.\n\n"
                    "If you are young, you are not on the sidelines. If you lead young people, you are "
                    "standing on holy ground."
                ),
                "image_fallback": "prayer-youth-leader.jpg",
                "is_featured": True,
            },
            {
                "title": "Be a Powerful Witness",
                "category": "faith",
                "excerpt": "The Gospel is still the power of God. The world is waiting for a Church that believes it.",
                "body": (
                    "Evangelism is not a personality type. It is the overflow of a life that has encountered Jesus.\n\n"
                    "Across India, Pakistan, and the United States, the mission remains the same: to make "
                    "Christ known, to strengthen believers, and to raise witnesses.\n\n"
                    "Ask God to open your eyes to the people already around you."
                ),
                "image_fallback": "prayer-congregation.jpg",
                "is_featured": True,
            },
            {
                "title": "Lead From the Secret Place",
                "category": "leadership",
                "excerpt": "Influence without intimacy with Christ is a heavy burden. Leadership begins in prayer.",
                "body": (
                    "The world trains leaders to be impressive. The Kingdom trains leaders to be faithful.\n\n"
                    "Whether you lead a team, a family, a youth group, or a church, the first assignment "
                    "is to remain close to Jesus.\n\n"
                    "From that place, He will send you."
                ),
                "image_fallback": "hero-preaching.jpg",
                "is_featured": True,
            },
        ]
        for i, data in enumerate(articles):
            Article.objects.update_or_create(
                slug=data["title"].lower().replace(" ", "-")[:50],
                defaults={
                    **data,
                    "published_at": today - timedelta(days=i * 7),
                    "is_published": True,
                },
            )

        messages = [
            {
                "title": "Raise a Generation That Knows Christ",
                "description": "A call to mentor, disciple, and send the next generation as witnesses for Jesus.",
                "thumbnail_fallback": "hero-preaching.jpg",
                "is_featured": True,
            },
            {
                "title": "Identity Before Assignment",
                "description": "You cannot walk in calling until you rest in who you are in Christ.",
                "thumbnail_fallback": "speaking-jesus-calls.jpg",
                "is_featured": False,
            },
            {
                "title": "A Message Without Borders",
                "description": "The Gospel is not limited by culture, language, or nation. Christ is Lord of all.",
                "thumbnail_fallback": "speaking-uturn.jpg",
                "is_featured": False,
            },
        ]
        for i, data in enumerate(messages):
            Message.objects.update_or_create(
                slug=data["title"].lower().replace(" ", "-")[:50],
                defaults={
                    **data,
                    "preached_on": today - timedelta(days=i * 14),
                    "is_published": True,
                },
            )

        events = [
            {
                "title": "Next Generation Night",
                "event_type": "youth",
                "location": "Bangalore, India",
                "description": "An evening of worship, Word, and mentoring for young people hungry to walk with Jesus.",
            },
            {
                "title": "Leadership & Discipleship Gathering",
                "event_type": "leadership",
                "location": "Hyderabad, India",
                "description": "Equipping believers to grow spiritually and influence others with humility and courage.",
            },
            {
                "title": "Weekend of Encouragement",
                "event_type": "church",
                "location": "Invited church — United States",
                "description": "A special weekend of teaching, prayer, and calling people to know Christ and make Him known.",
            },
        ]
        now = timezone.now()
        for i, data in enumerate(events):
            Event.objects.update_or_create(
                slug=data["title"].lower().replace(" ", "-")[:50],
                defaults={
                    **data,
                    "starts_at": now + timedelta(days=21 + i * 18),
                    "is_published": True,
                },
            )

        testimonies = [
            {
                "name": "Rahul",
                "location": "Bengaluru, India",
                "story": (
                    "I came looking for direction and found Jesus. Through mentoring I began to understand "
                    "that my life has a calling, and that I can be a witness in my workplace."
                ),
            },
            {
                "name": "Ayesha",
                "location": "Karachi, Pakistan",
                "story": (
                    "Prayer and the Word restored my hope. I learned that God still speaks, still heals, "
                    "and still sends ordinary people."
                ),
            },
            {
                "name": "Daniel",
                "location": "Dallas, United States",
                "story": (
                    "I was reminded that leadership is stewardship. The call to raise, equip, and send "
                    "gave language to what God had already been stirring in my heart."
                ),
            },
        ]
        for data in testimonies:
            Testimony.objects.update_or_create(
                name=data["name"],
                location=data["location"],
                defaults={**data, "is_approved": True},
            )

        self.stdout.write(self.style.SUCCESS("Sample ministry content is ready."))
