# Raspberry Pi Full Stack with Raspbian

This repository contains a fork of the repository that contains the complete code from the course Raspberry Pi:Full Stack with Raspbian, from Tech Explorations with additions documented below.

You can find more information on [ Raspberry Pi: Full Stack Raspbian here](https://app.techexplorations.com/courses/raspberry-pi-full-stack-raspbian/?mwr=49bc8a3f).

The objective of this course is to take you to a whirlwind tour of the Raspberry Pi, and introduce you to everything that is great about it.

Structured as a project, you will become familiar with the various components that make up the web development stack: the operating system, the hardware (including the GPIOs), the application server, web server, database server, and the Python programming language.

You will also become familiar with Cloud services that you will integrate into your Raspberry Pi-powered web application.

You application will take sensor data and make them available to the user via a web interface that is constructed based on jQuery and HTML5.

You will need a Raspberry Pi, a DHT22 sensor, a button, an LED, a few resistors and a breadboard.

If you have a Wifi USB dongle, you will learn how to set it up with your Raspberry Pi.

To make the most from this course, you should be familiar with basic programming and be comfortable with the command line.

# Enhancements and Corrections
## Remove Credentials from Source Code
If you plan to make your code available online like I did then you'll need to remove all credentials from the source code and create Linux environment variables instead by doing the following:

Files: env_log.py, rf24_receiver.py

Change this where <YOUR KEY VALUE> is the actual value of your IFTTT trigger key:

    requests.post("https://maker.ifttt.com/trigger/RPiFS_report/with/key/<YOUR IFTTT RPiFS REPORT KEY>", data=report)

to this:

    key_val = os.environ["IFTTT_RPIFS_REPORT_KEY"]
    req_link = f"https://maker.ifttt.com/trigger/RPiFS_report/with/key/{key_val}"
    requests.post(req_link, data=report)

NOTE: this change assumes that you've implemented the Text Messaging using Twilio portion of the project.  If you have not then add the following to the top of the files:

    import os

Add the following to the .bashrc files for the pi and root users.  The file can be found in the root directory for each user.

    export IFTTT_RPIFS_REPORT_KEY=<YOUR IFTTT RPiFS REPORT KEY>

Add the following to the [SERVICE] section of the rf24_receiver.service configuration file:

    Environment="IFTTT_RPIFS_REPORT_KEY=<YOUR IFTTT RPiFS REPORT KEY>"

Add the following to crontab file for the root user by executing the following commands:

    $ sudo su
    # crontab -e

Add the following to the file before list of defined cron jobs to provide access to the environment variable from the env_log.py file:

    IFTTT_RPIFS_REPORT_KEY=<YOUR IFTTT RPiFS REPORT KEY>

## Provide Access to Twilio Environment Variables to Environment Application

When I provided the write-up for the Raspberry Pi: Full Stack Raspbian book to Peter Dalmaris I neglected to mention that the Twilio environment variables need to be added to the crontab file for the root user to allow the environment application itself to access them.  Without this change, the application will not be able to trigger text messages when executed via cron.

Add the following to crontab file for the root user by executing the following commands:

    $ sudo su
    # crontab -e

Add the following to the file before list of defined cron jobs to provide access to the environment variable from the env_log.py file:

    TWILIO_ACCOUNT_SID=<YOUR TWILIO ACCOUNT SID>
    TWILIO_AUTH_TOKEN=<YOUR TWILIO AUTH>
    TWILIO_PHONE_NUMBER=<YOUR WILIO PHONE NUMBER>
    MY_PHONE_NUMBER=<YOUR PERSONAL PHONE NUMBER>

## Bash Script to Setup Temporary Twilio webhook

Occasionally you may need to test access between your web application and Twilio without using the full stack application by running the applicable Flask application on the command line.  When doing the webhook is modified to use he one setup by ngrok (as described in the Raspberry Pi: Full Stack Raspbian book).  When finished testing use the provided twilio_update_webhook bash script to change the webhokk back to the one needed by the full stack application.

Run the script as the pi user.

But, to use this script you will need to setup a couple of additional environment variables by adding the following to the .bashrc file for the pi user.

    export RPIFS_SERVER_URL=<YOUR FULL EXTERNAL URL>
    export RPIFS_SERVER_EXTERNAL_TCP_PORT=<YOUR EXTERNAL PORT NUMBER>
