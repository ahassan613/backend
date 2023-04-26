


# scenario1 = "First Name: john \
# Email: johnctas1@gmail.com \
# Phone: (770) 873-6338 \
# From Zip: 28203 \
# From City: Charlotte \
# From State: NC \
# To Zip: 30121 \
# To City: Cartersville \
# To State: GA \
# Make: Hyundai \
# Model: Elantra \
# Model Year: 2010 \
# Vehicle 1 Type: Car \
# Ship Date: 11/24/2021 \
# Transport Type: Open \
# Vehicle Condition: Not Running"
def leadsFunc(stringtxt):
    if 'first_name' in stringtxt:
        secnario2 = stringtxt
        full_name = secnario2.split('phone:')[0].replace("first_name:", "").replace("last_name:", "").strip()
        print(full_name)
        phone = secnario2.split('email:')[0].split(':')[-1].strip()
        print(phone)
        email = secnario2.split('pickup_city:')[0].split(':')[-1].strip()
        print(email)
        fromCity = secnario2.split('pickup_state_code:')[0].split(':')[-1].strip()
        print(fromCity)
        fromState = secnario2.split('pickup_zip:')[0].split(':')[-1].strip()
        print(fromState)
        fromZip = secnario2.split('dropoff_city:')[0].split(':')[-1].strip()
        print(fromZip)
        toCity = secnario2.split('dropoff_state_code:')[0].split(':')[-1].strip()
        print(toCity)
        toState = secnario2.split('dropoff_zip:')[0].split(':')[-1].strip()
        print(toState)
        toZip = secnario2.split('estimated_ship_date:')[0].split(':')[-1].strip()
        print(toZip)
        shipDate = secnario2.split('vehicle_runs:')[0].split(':')[-1].strip()
        print(shipDate)
        vehicleRuns = secnario2.split('ship_via_id:')[0].split(':')[-1].strip()
        print(vehicleRuns)
        transportType = secnario2.split('year1:')[0].split(':')[-1].strip()
        print(transportType)
        modelYear = secnario2.split('make1:')[0].split(':')[-1].strip()
        print(modelYear)
        maker = secnario2.split('model1:')[0].split(':')[-1].strip()
        print(maker)
        model = secnario2.split('vehicle_type_id1:')[0].split(':')[-1].strip()
        print(model)
        vehicleType = secnario2.split('vehicle_type_id1:')[1].strip()
        print(vehicleType)
    else:
        print("in else")
        scenario1 = stringtxt
        first_name = scenario1.split('Email:')[0].split(':')[1]
        print(first_name)
        Email = scenario1.split('Phone:')[0].split(':')[-1]
        print(Email)
        phone = scenario1.split('From Zip:')[0].split(':')[-1]
        print(phone)
        fromzip = scenario1.split('From City:')[0].split(':')[-1]
        print(fromzip)
        fromCity = scenario1.split('From State:')[0].split(':')[-1]
        print(fromCity)
        fromState= scenario1.split('To Zip:')[0].split(':')[-1]
        print(fromState)
        toZip= scenario1.split('To City:')[0].split(':')[-1]
        print(toZip)
        toCity= scenario1.split('To State:')[0].split(':')[-1]
        print(toCity)
        toState = scenario1.split('Make:')[0].split(':')[-1]
        print(toState)
        carmaker = scenario1.split('Model:')[0].split(':')[-1]
        print(carmaker)
        carModel = scenario1.split('Model Year:')[0].split(':')[-1]
        print(carModel)
        modelYear = scenario1.split('Vehicle 1 Type:')[0].split(':')[-1]
        print(modelYear)
        vechleType =  scenario1.split('Ship Date:')[0].split(':')[-1]
        print(vechleType)
        ShipDate =  scenario1.split('Transport Type:')[0].split(':')[-1]
        print(ShipDate)
        tansportType =  scenario1.split('Vehicle Condition:')[0].split(':')[-1]
        print(tansportType)
        vechileCondition = scenario1.split('Vehicle Condition:')[1]
        print(vechileCondition)


secnario2 = "\
last_name: Laster \
phone: (216) 647-4223 \
email: monicalaster777@gmail.com \
pickup_city: Albuquerque \
pickup_state_code: NM  \
pickup_zip: 87109 \
dropoff_city: Cleveland \
dropoff_state_code: OH \
dropoff_zip: 44113 \
estimated_ship_date: 11/23/2021 \
vehicle_runs: Yes \
ship_via_id: Open \
year1: 2010 \
model1: Patriot \
vehicle_type_id1: SUV"


scenario1 = "First Name: Kendrick \
        \
        Phone: (816) 255-7372 \
        From Zip: 85381 \
        From City: Peoria \
        From State: AZ \
        To Zip: 64133 \
        To City: Raytown \
        To State: MO \
        Make: Pontiac \
        Model: Grand Prix \
        Model Year: 2004 \
        Vehicle 1 Type: Car \
        Ship Date: 12/28/2021 \
         \
        Vehicle Condition: Running"

leadsFunc(secnario2)
