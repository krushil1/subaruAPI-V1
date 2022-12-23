
## Description

Subaru API built with [subarulink package](https://github.com/G-Two/subarulink). Current version built in Flask and can lock and unlock your Subaru that is subscribed to the Starlink services.

## Credits
Used code from [aws-subaru-api](https://github.com/chrisroedig/aws-subaru-api) repository to convert [chrisroedig's](https://github.com/chrisroedig) repository into a Flask app.

## Installation

Clone the project

```bash
  git clone https://github.com/krushil1/subaruAPI-V1.git
```

Go to the project directory

```bash
  cd subaruAPI-V1
```

Setup virtual environment

```bash
  python3 -m venv env
  source env/bin/activate
```

Enter your credentials inside the [subaru_link_service.py](https://github.com/krushil1/subaruAPI-V1/blob/main/subaru_link_service.py) file

```bash
    SUBARU_USERNAME=""
    SUBARU_PASSWORD=""
    SUBARU_DEVICE_ID="" # For device, use an 10 digit number. Ex: timestamp
    SUBARU_DEVICE_NAME="subarulink"
    SUBARU_VIN=""
    SUBARU_PIN=""
```


Install the dependencies

```bash
  pip install -r requirements.txt
```

Testing the server locally
```bash
  python3 flaskapp.py
```

### Using the server for sending unlock/lock requests

#### To unlock your Subaru
```
POST Request
Host: serverURL
Content-Type: application/json

{
  "pin": "XXXX",
  "command": "unlock",
}
```

#### To lock your Subaru
```
POST Request
Host: serverURL
Content-Type: application/json

{
  "pin": "XXXX",
  "command": "lock",
}
```

## Deploying the Flask server
Create an account on [Vercel](https://vercel.com/) for deploying it to a live server!