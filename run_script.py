#!/usr/bin/env python3
import json
import csv

# initialize django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'arcticapi.settings'
import django
django.setup()

# regular imports
from api.models import Campaign

# main script
def main():
    # Copy campaigns
    with open('campaigns_for_management.csv', newline='', encoding="utf8") as f:
        reader = csv.reader(f)
        campaigns = list(reader)
        for item in campaigns:
            if item[1] != "url":
                # Create a campaign object
                campaign = Campaign()

                # Add the columns for that row to the campaign object
                campaign.url = item[1]
                campaign.campaign_id = item[2]
                campaign.auto_fb_post_mode = item[3]
                campaign.collected_date = item[4]
                campaign.category_id = item[5]
                campaign.category = item[6]
                campaign.currencycode = item[7]
                campaign.current_amount = item[8]
                campaign.goal = item[9]
                campaign.donators = item[10]
                campaign.days_active = item[11]
                campaign.days_created = item[12]
                campaign.title = item[13]
                campaign.description = item[14]
                campaign.default_url = item[15]
                campaign.has_beneficiary = item[16]
                campaign.media_type = item[17]
                campaign.project_type = item[18]
                campaign.turn_off_donations = item[19]
                campaign.user_id = item[20]
                campaign.user_first_name = item[21]
                campaign.user_last_name = item[22]
                campaign.user_facebook_id = item[23]
                campaign.user_profile_url = item[24]
                campaign.visible_in_search = item[25]
                campaign.status = item[26]
                campaign.deactivated = item[27]
                campaign.state = item[28]
                campaign.is_launched = item[29]
                campaign.campaign_image_url = item[30]
                campaign.created_at = item[31]
                campaign.launch_date = item[32]
                campaign.campaign_hearts = item[33]
                campaign.social_share_total = item[34]
                campaign.social_share_last_udpate = item[35]
                campaign.location_city = item[36]
                campaign.location_country = item[37]
                campaign.location_zip = item[38]
                campaign.is_charity = item[39]
                campaign.charity_valid = item[40]
                campaign.charity_npo_id = item[41]
                campaign.charity_name = item[42]
                campaign.velocity = item[43]
                campaign.overall_popularity = item[44]
                campaign.percent_goal_complete = item[45]
                campaign.avg_donation_per_donor = item[46]

                print(campaign)

                # Save the campaign object to the database
                campaign.save()