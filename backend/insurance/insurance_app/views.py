import json
import os
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import JsonResponse
import subprocess
from insurance_app.site_utils.user import UserProfile
from insurance_app.site_utils.companies import Companies, InsuranceCompany


GENERATE_BINARY_PATH = './host'
VALIDATE_BINARY_PATH = './verifier'

companies = Companies()
offers = [
    {
        "title": "Comfort Plan",
        "description": "Our Comfort Plan provides essential coverage for your everyday needs. It includes basic protection for your vehicle and third-party liability, ensuring peace of mind for your daily commute."
    },
    {
        "title": "Plus Plan",
        "description": "The Plus Plan offers enhanced protection beyond the basics. It includes comprehensive coverage for your vehicle, plus additional benefits like roadside assistance and a courtesy car. This plan is perfect for those who want extra security without breaking the bank."
    },
    {
        "title": "Extra Plan",
        "description": "Our Extra Plan takes your coverage to the next level with premium features. It includes all the benefits of the Plus Plan, along with coverage for personal belongings in your vehicle and enhanced medical expenses. This plan is ideal for families and those who use their vehicle extensively."
    },
    {
        "title": "Premium Plan",
        "description": "The Premium Plan is our most comprehensive offering, designed for those who want the ultimate in protection and service. It includes all lower-tier benefits plus unique features like zero depreciation cover and protection against uninsured drivers. With 24/7 premium support, this plan ensures you're always taken care of, no matter what happens."
    }
]


def generate_and_verify_zkproof(request, company_id):
	if request.method == "GET":
		try:

			driving_data_dict = {
				"overall_average_travel_time_in_min": 45,
				"overall_average_fuel_consumption": 7,
				"overall_average_electric_consumption": 2,
				"overall_average_speed_in_kmph": 96,
				"total_distance_traveled": 4500,
				"number_of_hard_brakes_per_1000km": 3,
				"number_of_rash_drives_per_1000km": 2,
				"ins_tear": 2
			}

			# Step 3: Save JSON data to a temporary file
			json_file_path = os.path.join('./', 'user.json')  # Temporary JSON file path
			with open(json_file_path, 'w') as json_file:
				json.dump(driving_data_dict, json_file)

			# Step 4: Run the first binary (ZKProof generation) with the JSON file as input
			generate_result = subprocess.run([GENERATE_BINARY_PATH], capture_output=True, text=True)
			
			if generate_result.returncode != 0:
				return JsonResponse({"status": "error", "message": "Failed to generate ZKProof", "output": generate_result.stderr}, status=500)
			
			# Extract the price from the generation output
			generation_output = generate_result.stdout.strip()
			price = generation_output

			# Step 5: Run the second binary (ZKProof validation)
			validate_result = subprocess.run([VALIDATE_BINARY_PATH], capture_output=True, text=True)
			
			if validate_result.returncode == 0:
				# Success: Return both generation and validation outputs, including the price
				output =  JsonResponse({
					"status": "success", 
					"generate_output": generation_output, 
					"validation_output": validate_result.stdout,
					"price": price
				})
				companies.calculate_price(price)
				return render(request, "Insurance_offer.html", {
        				'company_id': company_id,
        				'company': companies.companies[company_id],
        				'offers': offers,
						'calc_price': price
    				})



			else:
				return JsonResponse({"status": "error", "message": "ZKProof validation failed", "output": validate_result.stderr}, status=500)
		
		except Exception as e:
			return JsonResponse({"status": "error", "message": str(e)}, status=500)
	
	return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)



def home(request):
    return render(request, 'index.html')

def insurance(request):
    profile = UserProfile()
    return render(request, "insurance.html", {
        'user': UserProfile,
        'companies': companies.companies
    })

def insurance_offer(request, company_id):
    return render(request, "Insurance_offer.html", {
        'company_id': company_id,
        'company': companies.companies[company_id],
        'offers': offers,
		'calc_price': (companies.companies[company_id].calculated_price)
    })
