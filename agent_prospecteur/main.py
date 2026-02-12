import argparse
import logging
import sys
import webbrowser
import time

# Easter Egg: Import Antigravity at start
try:
    import antigravity
    print("🚀 Décollage immédiat !")
except ImportError:
    pass

from config import Config
from db.database import Database
from search.google_places import GooglePlacesSearch
from detector.site_checker import SiteChecker
from detector.design_analyzer import DesignAnalyzer
from enrich.email_finder import EmailFinder
from message.generator import MessageGenerator
from sender.email_sender import EmailSender

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("prospector.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Agent Prospecteur IA")
    parser.add_argument("--search", type=str, default="bakery", help="Keyword to search for (e.g. bakery)")
    parser.add_argument("--location", type=str, default="48.8566,2.3522", help="Lat,Long coordinates")
    parser.add_argument("--radius", type=int, default=5000, help="Search radius in meters")
    parser.add_argument("--domain", type=str, help="Specific business domain/type (e.g. restaurant, plumber)")
    parser.add_argument("--dry-run", action="store_true", help="Run without sending emails")
    
    args = parser.parse_args()

    # Flight Mode Check
    if Config.ANTIGRAVITY_FLIGHT:
        logger.info("✈️  MODE FLIGHT ACTIVE: Using mock data, no real API calls.")

    # Initialize Modules
    db = Database(Config.DB_PATH)
    db.connect()
    
    searcher = GooglePlacesSearch()
    site_checker = SiteChecker()
    analyzer = DesignAnalyzer()
    enricher = EmailFinder()
    generator = MessageGenerator()
    sender = EmailSender()

    # 1. Search Prospects
    logger.info(f"🔎 Searching for '{args.search}' in radius {args.radius}m...")
    prospects = searcher.search(
        location=args.location, 
        radius=args.radius, 
        keyword=args.search,
        type=args.domain
    )
    
    logger.info(f"Found {len(prospects)} potential prospects.")
    
    processed_count = 0
    sent_count = 0

    for p in prospects:
        logger.info(f"\nAnalyzing prospect: {p['name']}")
        
        # 2. Check Website
        website_status = "UNKNOWN"
        url = p.get('website')
        
        if not url:
            # Try to guess
            guessed_url = site_checker.guess_domain(p['name'])
            if guessed_url:
                logger.info(f"  Url guessed: {guessed_url}")
                url = guessed_url
            else:
                logger.info("  No website found.")
                website_status = "NO_SITE"
        
        reasons = []
        if url:
            is_up, final_url, html = site_checker.check(url)
            if is_up:
                # 3. Analyze Design
                website_status, reasons = analyzer.analyze(html)
                logger.info(f"  Website status: {website_status} ({reasons})")
            else:
                logger.info("  Website check failed (down or timeout).")
                website_status = "NO_SITE" # Treat as no site if down? Or separate status? Let's say NO_SITE for now.

        # Filter: Keep only ARCHAIC or NO_SITE
        if website_status not in ['ARCHAIC', 'NO_SITE']:
            logger.info("  Skipping: Website is MODERN or UNKNOWN.")
            continue

        # 4. Enrich Email
        logger.info("  Enriching contact info...")
        email = enricher.find(url.split('//')[-1].split('/')[0] if url else None, p['name'])
        
        if not email:
            logger.warning("  No email found. Skipping auto-send.")
            # Save to DB for manual review?
             # For this task, we skip if no email, but we could save it.
        else:
            logger.info(f"  Email found: {email}")

        # 5. Generate & Send Message
        if email:
            prospect_data = {
                'name': p['name'],
                'city': p.get('address', '').split(',')[-1].strip(), # Crude city extraction
                'sector': args.domain or args.search,
                'website_status': website_status,
                'valid_reasons': reasons
            }
            
            message_body = generator.generate(prospect_data)
            subject = f"Optimisation de votre présence web - {p['name']}"
            
            if args.dry_run:
                logger.info("  [DRY RUN] Would send email:")
                logger.info(f"  To: {email}")
                logger.info(f"  Subject: {subject}")
                # logger.info(f"  Body: {message_body}") # Verbose
                sent = False # Didn't actually send
            else:
                sent = sender.send(email, subject, message_body)
                if sent:
                    logger.info("  ✅ Email sent successfully.")
                    sent_count += 1
                else:
                    logger.error("  ❌ Failed to send email.")

        # 6. Persist
        db.add_prospect({
            'name': p['name'],
            'address': p['address'],
            'city': p.get('address', '').split(',')[-1].strip(),
            'sector': args.domain or args.search,
            'website_url': url,
            'website_status': website_status,
            'email': email,
        })
        
        processed_count += 1
        
        # Easter Egg threshold
        if sent_count == 50:
             logger.info("🎉 50 Emails Sent! Triggering celebration...")
             try:
                 antigravity.geohash(37.421542, -122.085589, b'dow jones industrial average') # Just calling something from it
                 webbrowser.open("https://xkcd.com/353/")
             except:
                 pass

    logger.info(f"\nDone. Processed {processed_count} prospects. Sent {sent_count} emails.")
    db.close()

if __name__ == "__main__":
    main()
