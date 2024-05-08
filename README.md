# Food 'n Stuff Scheduler

FoodnStuffScheduler is an open-source Flask-based app designed to schedule, manage and coordinate volunteer activities efficiently for Trinity College's food pantry, "Food 'n Stuff". This project allows volunteers to sign up and for admins to post shifts and manage their hours.

  ![Logo](https://github.com/HamimMahdie/FoodnStuffscheduler/assets/144726390/a60db608-5f66-4275-b930-8f63d17dc2c8)  



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have Python or Python3 and `pip` or `pip3` installed on your system. 

### Cloning the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/HamimMahdie/FoodnStuffscheduler.git
```
```bash
cd FoodnStuffscheduler
```

### Setting Up the Virtual Environment

Create and activate a new virtual environment:

```bash
python -m venv env
```
```bash
source env/bin/activate
```

### Installing Dependencies

Install all required packages using `pip`. If a `requirements.txt` file is present, use it:

```bash
pip install -r requirements.txt
```

If you still encounter errors, install the necessary packages individually:

```bash
pip install Flask
```
```bash
pip install flask_mail
```

### Running the Application

Run the application using:

```bash
python app.py
```

### Accessing the Application

Open your web browser and visit:

```
http://localhost:5003
```

to start using the FoodnStuffScheduler.

### Utilizing the Google's SMTP API for email service

To use the **"Donate"** functionality, please swap the placeholders in app.py with an server email and an app password generated from Google that will serve the donation notifications. For more information, visit https://support.google.com/a/answer/176600?hl=en

## Features

- **Login/Register**: Login or register with credentials.
- **Admin Dashboard**: Admins can post new shifts and view reports.
- **Volunteer Dashboard**: Volunteers can view and sign up for shifts.
- **Donation Email Notifications**: Supports automated emails to Administrator for donations submitted by patrons.

## Contributing

Contributions are what make the **open-source** community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Please check out CONTRIBUTING.md for detailed guidelines. 

## Authors
- **Josh Ames** 
- **Hamim Mahdie** 
- **Benedicte Baile** 
- **Yusuke Abe** 
- **Hallie Bruno** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

