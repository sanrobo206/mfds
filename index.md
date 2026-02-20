---
layout: home
title: Mobile Fire Detection System
---

<div style="width: 100%; margin: 0; padding: 80px 40px; font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; color: #111; background-color: #ffffff; box-sizing: border-box; line-height: 1.8;">

  <!-- Header Section -->
  <header style="text-align: center; margin-bottom: 80px;">
    <h1 style="font-size: 3.5rem; font-weight: 800; color: #000; margin-bottom: 10px; letter-spacing: -0.05em; text-transform: uppercase;">
      Mobile Fire Detection System
    </h1>
    <p style="font-size: 1.5rem; color: #666; font-weight: 400; margin-top: 0;">
      by Sanatan Sinha
    </p>
  </header>

  <!-- Hero Image -->
  <div style="text-align: center; margin-bottom: 80px; max-width: 1100px; margin-left: auto; margin-right: auto;">
    <img src="docs/rover-cad.png" alt="Rover CAD Model" style="width: 100%; border-radius: 12px; box-shadow: 0 20px 50px rgba(0,0,0,0.12); border: 1px solid #eee;">
  </div>

  <hr style="border: 0; border-top: 1px solid #eaeaea; margin: 60px 0;">

  <!-- Overview Section -->
  <section style="max-width: 950px; margin: 0 auto 100px auto;">
    <h2 style="font-size: 2.8rem; font-weight: 700; color: #000; margin-bottom: 40px; text-align: center;">Overview</h2>
    <div style="font-size: 1.25rem; color: #333; text-align: justify;">
      The project investigated how making a mobile fire detection system could be a big improvement in response time than the conventional fire alarm system. The goal of the project was to make a mobile fire detection system which could not only detect the fire or signs of fire but also give the status of the house and can be remotely controlled, even when away. There was a web browser based website which would constantly give the status of the house when there was no fire, but if there was fire or any sign of fire, there would be a notification.
      <br><br>
      The testing first occurred in the house, then if the majority of the time the system was able to detect the fire and then give the notification, the testing occurred in the forest. The rover (the part that made the system mobile) was capable of climbing up and down the stairs and had 6 wheels. Not only was the ability to detect and give a notification of the fire going to be tested, but also the rover's ability to climb the stairs was going to be assessed. Both of the factors determined if this system passed or didn't pass. Because the rover might be limited to being terrestrial, a further improvement that could be made so every area in the forest could be monitored, was making a drone that could get launched from the rover (which would be improved so that it could be used as a launchpad for the drone), and then do surveillance over the forest. 
      <br><br>
      <b>Keywords:</b> Mobile fire detection system, rover, drone, fire alarm, surveillance
    </div>
  </section>

  <!-- Problem Statement Section (Glassmorphism) -->
  <section style="max-width: 950px; margin: 0 auto 100px auto; background: #fcfcfc; padding: 60px; border-radius: 24px; border: 1px solid #f1f1f1;">
    <h2 style="font-size: 2.2rem; font-weight: 700; color: #000; margin-bottom: 30px;">Mechanical Design & Safety</h2>
    <div style="font-size: 1.2rem; color: #444; line-height: 1.9;">
      As of now, the majority of the fires tend to occur in the kitchen and in dry forests which is a really big hazard. More than 40 percent of the fires occur due to leaving the kitchen unattended, and can lead to many devastating effects that are hard to recover (NFPA, 2025). When the house is unattended, a fire alarm is ineffective. Even though the fire alarm is really loud, there is no notification system in order to notify the person if they are away, which makes it really hard to get an immediate response to the situation.
      <br><br>
      A solution is to make a mobile fire detection system that includes a stair-climbing rover and one robot arm that has multiple fire detection sensors and has a camera. Unlike fire alarms, this approach can use computer vision including a <b>YOLO model</b> to detect the fire or any signs of fire, so that it can be dealt with before the situation gets worse.
    </div>
  </section>

  <!-- Key Features Grid -->
  <section style="max-width: 1000px; margin: 0 auto 100px auto;">
    <h2 style="font-size: 2.5rem; font-weight: 700; color: #000; margin-bottom: 40px; text-align: center;">Key Features</h2>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
      <div style="padding: 30px; background: #fff; border: 1px solid #eee; border-radius: 15px;">
        <b>Dual Base Controllers</b>: Primary and secondary motor controllers for six-wheel drive system.
      </div>
      <div style="padding: 30px; background: #fff; border: 1px solid #eee; border-radius: 15px;">
        <b>360° LiDAR Scanning</b>: Slamtec RPLidar A1M8 for real-time 360-degree mapping.
      </div>
      <div style="padding: 30px; background: #fff; border: 1px solid #eee; border-radius: 15px;">
        <b>Fire & Smoke Detection</b>: YOLOv8-based AI model for early fire and smoke detection.
      </div>
      <div style="padding: 30px; background: #fff; border: 1px solid #eee; border-radius: 15px;">
        <b>Web-Based Control</b>: Flask/SocketIO web interface for remote operation and live streaming.
      </div>
    </div>
  </section>

  <!-- Hardware Details (List Style) -->
  <section style="max-width: 950px; margin: 0 auto 100px auto;">
    <h2 style="font-size: 2.2rem; font-weight: 700; color: #000; border-bottom: 2px solid #eee; padding-bottom: 10px;">Hardware Components</h2>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-top: 30px;">
      <div>
        <h4 style="text-transform: uppercase; color: #666;">Chassis & Mobility</h4>
        <ul style="color: #444;">
          <li>6-Wheel Drive System</li>
          <li>Steering Servos (SCS-series)</li>
          <li>Rocker-Bogie Suspension</li>
        </ul>
      </div>
      <div>
        <h4 style="text-transform: uppercase; color: #666;">Computing</h4>
        <ul style="color: #444;">
          <li>Raspberry Pi Main Control Unit</li>
          <li>2x ESP32 Lower-level Controllers</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- Acknowledgments / License -->
  <footer style="margin-top: 150px; padding-top: 50px; border-top: 1px solid #eee; text-align: center; color: #aaa; font-size: 0.9rem;">
    <p>Project maintained by <b>Sanatan Sinha</b> (sanrobo206)</p>
    <p style="max-width: 800px; margin: 20px auto; line-height: 1.4;">
      Acknowledgments: Based on Waveshare UGV Rover, YOLOv8, and research from NFPA and Florida Atlantic University.
    </p>
    <div style="margin-top: 40px; font-weight: 700; color: #000; text-transform: uppercase; letter-spacing: 2px;">
      Created by Sanatan Sinha
    </div>
  </footer>

</div>
