from django.http import JsonResponse, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from PIL import Image
import numpy as np
import os
from .forms import CustomUserCreationForm, SteganographyForm
from .models import CustomUser

def home(request):
    return render(request, 'steganography/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'steganography/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_home')
        else:
            return render(request, 'steganography/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'steganography/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return render(request, 'steganography/logout.html')

@login_required
def user_home(request):
    return render(request, 'steganography/user_home.html')

def encode_message_in_image(image, text_file, filename):
    message = text_file.read().decode('utf-8') + "###END###"
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '00000000'
    image = Image.open(image)
    image = image.convert('RGB')
    np_image = np.array(image)
    message_index = 0
    for row in np_image:
        for pixel in row:
            for channel in range(3):
                if message_index < len(binary_message):
                    pixel[channel] = int(format(pixel[channel], '08b')[:-1] + binary_message[message_index], 2)
                    message_index += 1
                else:
                    break 
    encoded_image = Image.fromarray(np_image)
    output_filename = f"{filename if filename else 'encoded_image'}.png"
    output_path = os.path.join("media", output_filename)
    encoded_image.save(output_path)
    return output_path, output_filename

def decode_message_from_image(image):
    image = Image.open(image)
    image = image.convert('RGB')
    np_image = np.array(image)
    binary_message = ''
    for row in np_image:
        for pixel in row:
            for channel in range(3):
                binary_message += format(pixel[channel], '08b')[-1]
    chars = [chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message)-8, 8)]
    message = ''.join(chars)
    if "###END###" in message:
        message = message.split("###END###")[0]
    text_file_path = "media/decoded_message.txt"
    with open(text_file_path, 'w', encoding="utf-8") as file:
        file.write(message)
    return text_file_path

def encode_view(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        text_file = request.FILES.get('text_file')
        filename = request.POST.get('filename')
        if image and text_file:
            output_image_path, output_filename = encode_message_in_image(image, text_file, filename)
            return render(request, 'steganography/encode_success.html', {'filename': output_filename})
    return render(request, 'steganography/encode.html')

def decode_view(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image:
            text_file_path = decode_message_from_image(image)
            response = HttpResponse(open(text_file_path, 'rb').read(), content_type="text/plain")
            response['Content-Disposition'] = 'attachment; filename="decode_message.txt"'
            return response
    return render(request, 'steganography/decode.html')
