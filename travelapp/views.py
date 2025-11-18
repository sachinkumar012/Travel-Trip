from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm,HotelForm,FlightForm,ChoiceForm,SeatForm,RoomForm,CityForm,PassengerDetailsForm
from .models import Flights,Hotels,Famous,BookFlight,BookHotel,BookPackage,City,Passenger

# Create your views here.

def IndexView(request):
    return render(request,'index.html')

def PackageView(request):
    form = FlightForm(request.POST)
    if request.method=="POST":
        if form.is_valid():
            source = form.cleaned_data['source'].upper()
            date = form.cleaned_data['date']
            destination = form.cleaned_data['destination'].upper()
            # city = destination
            flights = Flights.objects.filter(source=source).filter(destination=destination)
            famplace = Famous.objects.filter(city__city__contains=destination)
            hotels = Hotels.objects.filter(city__city__contains=destination)
            j = hotels[0].city if hotels.exists() else None
            s = {'source':source}
            c = {'city':j}
            f = {'Flights':flights}
            d = {'date':date}
            h = {'Hotels':hotels}
            fp = {'Famplace':famplace}
            form = {'form': form}
            form1 = {'form1':form}
            response = {**f,**s,**h,**fp,**form,**d,**c}
            return render(request,'package.html',response)
    else:
        return render(request,'package.html',{'form': form})


def registerView(request):
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_url')
    else:
            form=SignUpForm()
    return render(request,'registration/register.html',{'form': form})

def HotelView(request):
    form = HotelForm(request.POST)
    if request.method=="POST":
        if form.is_valid():
            city = form.cleaned_data['city'].upper()
            date = form.cleaned_data['date']
            hotels = Hotels.objects.filter(city__city__contains=city)
            d = {'date':date}
            h = {'Hotels':hotels}
            form = {'form': form}
            response = {**h,**d,**form}
            return render(request,'hotels.html',response)
        else:
            return render(request,'hotels.html',{'form': form})

    else:
        return render(request,'hotels.html',{'form': form})

def FlightView(request):
    form = FlightForm(request.POST)
    c = 0;
    if request.method=="POST":
        if form.is_valid():
            source = form.cleaned_data['source'].upper()
            destination = form.cleaned_data['destination'].upper()
            date = form.cleaned_data['date']
            flights = Flights.objects.filter(source__iexact=source, destination__iexact=destination)
            d = {'date':date}
            f = {'Flights':flights}
            form = {'form': form}
            response = {**f,**d,**form}
            return render(request,'flights.html',response)
        else:
            return render(request,'flights.html',{'form': form})
    else:
        return render(request,'flights.html',{'form': form})

@login_required
def Dashboard(request):
    user = request.user
    f1 = BookFlight.objects.filter(username_id=user)
    h1 = BookHotel.objects.filter(username_id=user)
    p1 = BookPackage.objects.filter(username_id=user)
    f={'flights':f1}
    h={'hotels':h1}
    p={'packages':p1}
    response= {**f,**h,**p}
    return render(request,'dashboard.html',response)

@login_required
def Flightbook(request,flight_num=None,date=None):
    cs=0
    c = None
    price = 0;
    form = SeatForm(request.POST)
    if request.method=="POST":
        if form.is_valid():
            flight = Flights.objects.filter(flight_num=flight_num)
            seats = form.cleaned_data['seats']
            # d1=datetime.datetime.strptime(date, "%Y-%m-%d").date()
            for i in flight:
                c = BookFlight.objects.filter(flight=i.flight_num).filter(date=date)
                d = BookPackage.objects.filter(flight=i.flight_num).filter(date=date)
                price = seats*i.eprice
                seatrem = i.seats
            for j in c:
                cs = cs + j.seat
            for k in d:
                cs = cs + k.seat
            seatrem = seatrem - cs
            if (seatrem-seats) > 0:
                avail = "available"
            else:
                avail = "unavailable"
            a = {'availability':avail}
            p = {'price':price}
            sb = {'seatsreq':seats}
            s = {'seatrem':seatrem}
            b = {'flight':flight}
            f = {'form':form}
            d = {'date':date}
            response = {**b,**d,**f,**s,**a,**sb,**p}
            print(s)
            return render(request,'bookflight.html',response)
        else:
            return render(request,'bookflight.html',{'form':form})
    else:
        return render(request,'bookflight.html',{'form':form})

@login_required
def FlightSubmit(request,flight_num=None,date=None,seat=None):
    # Show confirmation page with passenger details form
    form = PassengerDetailsForm(request.POST or None)
    flight = Flights.objects.filter(flight_num=flight_num).first()
    price = 0
    if flight:
        price = seat * flight.eprice
    
    if request.method == "POST":
        if form.is_valid():
            user = request.user
            b = BookFlight(
                username_id=user,
                flight=flight_num,
                date=date,
                seat=seat,
                passenger_name=form.cleaned_data['passenger_name'],
                passenger_email=form.cleaned_data['passenger_email'],
                passenger_phone=form.cleaned_data['passenger_phone'],
                passenger_address=form.cleaned_data['passenger_address'],
                passenger_id_number=form.cleaned_data.get('passenger_id_number', '')
            )
            b.save()
            return redirect('dashboard')
    
    context = {
        'form': form,
        'flight': flight,
        'flight_num': flight_num,
        'date': date,
        'seat': seat,
        'price': price
    }
    return render(request, 'confirmflight.html', context)

@login_required
def Hotelbook(request,hotel=None,date=None):
    cs=0
    c = None
    price = 0;
    form = RoomForm(request.POST)
    if request.method=="POST":
        if form.is_valid():
            room = form.cleaned_data['rooms']
            hotel = Hotels.objects.filter(hotel_name=hotel)
            # d1=datetime.datetime.strptime(date, "%Y-%m-%d").date()
            for i in hotel:
                c1 = BookHotel.objects.filter(hotel_name=i.hotel_name).filter(date=date)
                d1 = BookPackage.objects.filter(hotel_name=i.hotel_name).filter(date=date)
                price = room*i.hotel_price
                roomrem = i.rooms
            for j in c1:
                cs = cs + j.room
            for k in d1:
                cs = cs + k.room
            roomrem = roomrem - cs
            if (roomrem-room) > 0:
                avail = "available"
            else:
                avail = "unavailable"
            a = {'availability':avail}
            p = {'price':price}
            rb = {'roomreq':room}
            r = {'roomrem':roomrem}
            b = {'hotel':hotel}
            f = {'form':form}
            d = {'date':date}
            response = {**b,**d,**a,**p,**rb,**f,**r}
            return render(request,'bookhotel.html',response)
        else:
            return render(request,'bookhotel.html',{'form':form})
    else:
        return render(request,'bookhotel.html',{'form':form})

@login_required
def HotelSubmit(request,hotel=None,date=None,room=None):
    # Show confirmation page with guest details form
    form = PassengerDetailsForm(request.POST or None)
    hotel_obj = Hotels.objects.filter(hotel_name=hotel).first()
    price = 0
    if hotel_obj:
        price = room * hotel_obj.hotel_price
    
    if request.method == "POST":
        if form.is_valid():
            user = request.user
            b = BookHotel(
                username_id=user,
                hotel_name=hotel,
                date=date,
                room=room,
                guest_name=form.cleaned_data['passenger_name'],
                guest_email=form.cleaned_data['passenger_email'],
                guest_phone=form.cleaned_data['passenger_phone'],
                guest_address=form.cleaned_data['passenger_address'],
                guest_id_number=form.cleaned_data.get('passenger_id_number', '')
            )
            b.save()
            return redirect('dashboard')
    
    context = {
        'form': form,
        'hotel': hotel_obj,
        'hotel_name': hotel,
        'date': date,
        'room': room,
        'price': price
    }
    return render(request, 'confirmhotel.html', context)

@login_required
def PackageBook(request,source,city,date):
    roomrem=0
    price1=0
    cs = 0
    cs1 = 0
    price = 0
    seatrem = 0
    form = ChoiceForm(request.POST)
    allf = Flights.objects.filter(source=source).filter(destination=city)
    allh = Hotels.objects.filter(city__city__contains=city)
    af = {'allflights':allf}
    ah={'allhotels':allh}
    form1 = {'form': form}
    if request.method=="POST":
        if form.is_valid():
            flight = form.cleaned_data['flight'].upper()
            hotel = form.cleaned_data['hotel']
            seats = form.cleaned_data['seats']
            room = form.cleaned_data['rooms']
            flights = Flights.objects.filter(flight_num=flight)
            hotels = Hotels.objects.filter(hotel_name=hotel)
            # Initialize c and d as empty querysets
            c = BookFlight.objects.none()
            d = BookPackage.objects.none()
            for i in flights:
                c = BookFlight.objects.filter(flight=i.flight_num).filter(date=date)
                d = BookPackage.objects.filter(flight=i.flight_num).filter(date=date)
                price = seats*i.eprice
                seatrem = i.seats
            for j in c:
                cs = cs + j.seat
            for k in d:
                cs = cs + k.seat
            seatrem = seatrem - cs
            if (seatrem-seats) > 0:
                availf = "available"
            else:
                availf = "unavailable"

            # Initialize c1 and d1 as empty querysets
            c1 = BookHotel.objects.none()
            d1 = BookPackage.objects.none()
            for l in hotels:
                c1 = BookHotel.objects.filter(hotel_name=l.hotel_name).filter(date=date)
                d1 = BookPackage.objects.filter(hotel_name=l.hotel_name).filter(date=date)
                price1 = room*l.hotel_price
                roomrem = l.rooms
            for m in c1:
                cs1 = cs1 + m.room
            for n in d1:
                cs1 = cs1 + n.room
            roomrem = roomrem - cs1
            if (roomrem-room) > 0:
                availh = "available"
            else:
                availh = "unavailable"

            a = {'flavailability':availf}
            p = {'pricef':price}
            sb = {'seatsreq':seats}
            s = {'seatrem':seatrem}
            a1 = {'havailability':availh}
            p1 = {'priceh':price1}
            rb = {'roomreq':room}
            r = {'roomrem':roomrem}
            f = {'Flights':flights}
            h = {'Hotels':hotels}
            d = {'date':date}
            response = {**f,**af,**ah,**h,**d,**form1,**a,**a1,**p,**p1,**s,**sb,**r,**rb}
            return render(request,'bookpackage.html',response)
        else:
            response = {**af,**ah,**form1}
            return render(request,'bookpackage.html',response)
    else:
        response = {**af,**ah,**form1}
        return render(request,'bookpackage.html',response)

@login_required
def PackageSubmit(request,flight=None,hotel=None,date=None,seat=None,room=None):
    # Show confirmation page with passenger details form
    form = PassengerDetailsForm(request.POST or None)
    flight_obj = Flights.objects.filter(flight_num=flight).first()
    hotel_obj = Hotels.objects.filter(hotel_name=hotel).first()
    flight_price = 0
    hotel_price = 0
    total_price = 0
    
    if flight_obj:
        flight_price = seat * flight_obj.eprice
    if hotel_obj:
        hotel_price = room * hotel_obj.hotel_price
    total_price = flight_price + hotel_price
    
    if request.method == "POST":
        if form.is_valid():
            user = request.user
            try:
                b = BookPackage(
                    username_id=user,
                    flight=flight,
                    seat=seat,
                    hotel_name=hotel,
                    room=room,
                    date=date,
                    passenger_name=form.cleaned_data['passenger_name'],
                    passenger_email=form.cleaned_data['passenger_email'],
                    passenger_phone=form.cleaned_data['passenger_phone'],
                    passenger_address=form.cleaned_data['passenger_address'],
                    passenger_id_number=form.cleaned_data.get('passenger_id_number', '')
                )
                b.save()
                return redirect('dashboard')
            except Exception as e:
                from django.contrib import messages
                messages.error(request, f'Error booking package: {str(e)}')
                return redirect('dashboard')
    
    context = {
        'form': form,
        'flight': flight_obj,
        'hotel': hotel_obj,
        'flight_num': flight,
        'hotel_name': hotel,
        'date': date,
        'seat': seat,
        'room': room,
        'flight_price': flight_price,
        'hotel_price': hotel_price,
        'total_price': total_price
    }
    return render(request, 'confirmpackage.html', context)

@login_required
def CancelFlight(request,flight=None,date=None,seat=None):
    price = 0;
    flight = Flights.objects.filter(flight_num=flight)
    for i in flight:
        price = seat*i.eprice
    f = {'Flight':flight}
    p = {'price':price}
    s = {'seat':seat}
    d = {'date':date}
    response = {**f,**p,**s,**d}
    return render(request,'cancelflight.html',response)

@login_required
def ConfirmCancelFlight(request,flight=None,date=None,seat=None):
    user = request.user
    bookings = BookFlight.objects.filter(username_id=user).filter(flight=flight).filter(date=date).filter(seat=seat)
    # Delete associated passengers
    for booking in bookings:
        Passenger.objects.filter(booking_type='flight', booking_id=booking.id).delete()
    bookings.delete()
    return redirect('dashboard')

@login_required
def CancelHotel(request,hotel=None,date=None,room=None):
    hotel = Hotels.objects.filter(hotel_name=hotel)
    for i in hotel:
        price = room*i.hotel_price
    h = {'Hotel':hotel}
    p = {'price':price}
    r = {'room':room}
    d = {'date':date}
    response = {**h,**p,**r,**d}
    return render(request,'cancelhotel.html',response)

@login_required
def ConfirmCancelHotel(request,hotel=None,date=None,room=None):
    user = request.user
    bookings = BookHotel.objects.filter(username_id=user).filter(hotel_name=hotel).filter(date=date).filter(room=room)
    # Delete associated passengers
    for booking in bookings:
        Passenger.objects.filter(booking_type='hotel', booking_id=booking.id).delete()
    bookings.delete()
    return redirect('dashboard')

@login_required
def CancelPackage(request,flight=None,seat=None,hotel=None,date=None,room=None):
    flight = Flights.objects.filter(flight_num=flight)
    hotel = Hotels.objects.filter(hotel_name=hotel)
    for i in hotel:
        price = room*i.hotel_price
    for j in flight:
        price1 = seat*j.eprice
    f = {'Flight':flight}
    p = {'pricef':price1}
    s = {'seat':seat}
    h = {'Hotel':hotel}
    p1 = {'priceh':price}
    r = {'room':room}
    d = {'date':date}
    response = {**h,**p,**r,**d,**f,**p1,**s}
    return render(request,'cancelpackage.html',response)

@login_required
def ConfirmCancelPackage(request,flight=None,seat=None,hotel=None,date=None,room=None):
    user = request.user
    package = BookPackage.objects.filter(username_id=user).filter(hotel_name=hotel).filter(date=date).filter(room=room).filter(flight=flight).filter(seat=seat)
    # Delete associated passengers
    for pkg in package:
        Passenger.objects.filter(booking_type='package', booking_id=pkg.id).delete()
    package.delete()
    return redirect('dashboard')

@login_required
def ViewFlightDetails(request, booking_id):
    """View detailed information about a flight booking"""
    user = request.user
    try:
        booking = BookFlight.objects.get(id=booking_id, username_id=user)
        flight = Flights.objects.filter(flight_num=booking.flight).first()
        passengers = Passenger.objects.filter(booking_type='flight', booking_id=booking_id).order_by('passenger_number')
        
        context = {
            'booking': booking,
            'flight': flight,
            'passengers': passengers,
            'booking_type': 'flight'
        }
        return render(request, 'viewbooking.html', context)
    except BookFlight.DoesNotExist:
        return redirect('dashboard')

@login_required
def ViewHotelDetails(request, booking_id):
    """View detailed information about a hotel booking"""
    user = request.user
    try:
        booking = BookHotel.objects.get(id=booking_id, username_id=user)
        hotel = Hotels.objects.filter(hotel_name=booking.hotel_name).first()
        passengers = Passenger.objects.filter(booking_type='hotel', booking_id=booking_id).order_by('passenger_number')
        
        context = {
            'booking': booking,
            'hotel': hotel,
            'passengers': passengers,
            'booking_type': 'hotel'
        }
        return render(request, 'viewbooking.html', context)
    except BookHotel.DoesNotExist:
        return redirect('dashboard')

@login_required
def ViewPackageDetails(request, booking_id):
    """View detailed information about a package booking"""
    user = request.user
    try:
        booking = BookPackage.objects.get(id=booking_id, username_id=user)
        flight = Flights.objects.filter(flight_num=booking.flight).first()
        hotel = Hotels.objects.filter(hotel_name=booking.hotel_name).first()
        passengers = Passenger.objects.filter(booking_type='package', booking_id=booking_id).order_by('passenger_number')
        
        total_price = 0
        if flight:
            total_price += flight.eprice * booking.seat
        if hotel:
            total_price += hotel.hotel_price * booking.room
        
        context = {
            'booking': booking,
            'flight': flight,
            'hotel': hotel,
            'passengers': passengers,
            'booking_type': 'package',
            'total_price': total_price
        }
        return render(request, 'viewbooking.html', context)
    except BookPackage.DoesNotExist:
        return redirect('dashboard')

@login_required
def ManagePassengers(request, booking_type, booking_id):
    """Manage passengers for bookings with multiple seats/rooms"""
    user = request.user
    
    # Get the booking and verify ownership
    if booking_type == 'flight':
        booking = BookFlight.objects.filter(id=booking_id, username_id=user).first()
        num_passengers = booking.seat if booking else 0
    elif booking_type == 'hotel':
        booking = BookHotel.objects.filter(id=booking_id, username_id=user).first()
        num_passengers = booking.room if booking else 0
    elif booking_type == 'package':
        booking = BookPackage.objects.filter(id=booking_id, username_id=user).first()
        num_passengers = max(booking.seat, booking.room) if booking else 0
    else:
        return redirect('dashboard')
    
    if not booking:
        return redirect('dashboard')
    
    # Get existing passengers
    existing_passengers = Passenger.objects.filter(booking_type=booking_type, booking_id=booking_id).order_by('passenger_number')
    
    if request.method == 'POST':
        # Process form submission
        for i in range(1, num_passengers + 1):
            name = request.POST.get(f'passenger_name_{i}')
            email = request.POST.get(f'passenger_email_{i}')
            phone = request.POST.get(f'passenger_phone_{i}')
            address = request.POST.get(f'passenger_address_{i}')
            id_number = request.POST.get(f'passenger_id_number_{i}', '')
            
            if name and email and phone and address:
                passenger, created = Passenger.objects.update_or_create(
                    booking_type=booking_type,
                    booking_id=booking_id,
                    passenger_number=i,
                    defaults={
                        'passenger_name': name,
                        'passenger_email': email,
                        'passenger_phone': phone,
                        'passenger_address': address,
                        'passenger_id_number': id_number
                    }
                )
        
        return redirect('dashboard')
    
    # Prepare passenger data for form
    passengers_data = []
    for i in range(1, num_passengers + 1):
        existing = existing_passengers.filter(passenger_number=i).first()
        passengers_data.append({
            'number': i,
            'name': existing.passenger_name if existing else '',
            'email': existing.passenger_email if existing else '',
            'phone': existing.passenger_phone if existing else '',
            'address': existing.passenger_address if existing else '',
            'id_number': existing.passenger_id_number if existing else ''
        })
    
    context = {
        'booking': booking,
        'booking_type': booking_type,
        'booking_id': booking_id,
        'num_passengers': num_passengers,
        'passengers_data': passengers_data
    }
    
    if booking_type == 'flight':
        context['flight'] = Flights.objects.filter(flight_num=booking.flight).first()
    elif booking_type == 'hotel':
        context['hotel'] = Hotels.objects.filter(hotel_name=booking.hotel_name).first()
    elif booking_type == 'package':
        context['flight'] = Flights.objects.filter(flight_num=booking.flight).first()
        context['hotel'] = Hotels.objects.filter(hotel_name=booking.hotel_name).first()
    
    return render(request, 'managepassengers.html', context)

def PlacesView(request):
    form = CityForm(request.POST)
    if request.method=="POST":
        if form.is_valid():
            city = form.cleaned_data['city']
            famplace = Famous.objects.filter(city__city__contains=city)
            f = {'form':form}
            p = {'Famplace':famplace}
            response = {**f,**p}
            return render(request,'places.html',response)
        else:
            return render(request,'places.html',{'form':form})
    else:
        return render(request,'places.html',{'form':form})
