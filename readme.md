# Dating App Simulation

## Overview

This app simulates the behavior of users on a dating app. It is based on this [video](https://www.youtube.com/watch?v=x3lypVnJ0HM). The objective is to replicate the number of matches people get by considering their gender and the relative proportions of each gender in the simulation. Additionally, you have the option to modify the attractiveness equations for both genders and more. Predictably, the gender that is more abundant (typically men in reality) seems to face challenges in receiving likes or matches on dating apps.

## Features

- Simulate dating app behavior for men and women
- Customizable parameters for number of users, swipes, and attractiveness formula
- Generates statistics like mean and median for likes and matches
- Visualizes data through plots

## Installation

### Prerequisites

- Docker
- Docker Compose

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/Giminosk/dating-app-simulation.git
    ```

2. Navigate to the project folder:
    ```bash
    cd dating-app-simulation/app
    ```

3. Build and run the Docker container:
    ```bash
    docker-compose up --build
    ```

4. Open your web browser and go to `http://localhost:5000`.