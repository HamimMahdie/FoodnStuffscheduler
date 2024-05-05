# FoodnStuffScheduler

FoodnStuffScheduler is an open-source Flask-based app designed to schedule, manage and coordinate volunteer activities efficiently for Trinity College's food pantry, "Food 'n Stuff". This project allows volunteers to sign up and for admins to post shifts and manage their hours.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have Python or Python3 and `pip` or `pip3` installed on your system. 

### Cloning the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/HamimMahdie/FoodnStuffscheduler.git
cd FoodnStuffscheduler
```

### Setting Up the Virtual Environment

Create and activate a new virtual environment:

```bash
python3 -m venv env
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
pip install flask_mail
```

### Running the Application

Run the application using:

```bash
python3 app.py
```

### Accessing the Application

Open your web browser and visit:

```
http://localhost:5003
```

to start using the FoodnStuffScheduler.

## Features

- **Login/Register**: Login or register with credentials.
- **Admin Dashboard**: Admins can post new shifts and view reports.
- **Volunteer Dashboard**: Volunteers can view and sign up for shifts.
- **Donation Email Notifications**: Supports automated emails to Administrator for donations submitted by patrons.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

## Authors

-
- **Josh Ames** 
- **Hamim Mahdie** 
- **Benedicte Baile** 
- **Yusuke Abe** 
- **Hallie Bruno** 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

