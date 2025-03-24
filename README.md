# Image Steganography using Django

A web-based **Image Steganography** project built using **Django** that allows users to **hide secret messages inside images** and later extract them.

## ✨ Features
- **User Authentication** (Register, Login, Logout)
- **Encode Message** - Hide text inside an image
- **Decode Message** - Extract hidden text from an image
- **File Management** - Save encoded images securely
- **Modern UI** - Styled with **Bootstrap** and a sleek design
- **Security Features** - Limit file types & size

## Installation

### **Clone the Repository**
```bash
git clone https://github.com/yourusername/image-steganography-django.git
cd image-steganography-django

### **Database connection**
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

