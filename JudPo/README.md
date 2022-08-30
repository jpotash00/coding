Original App Design Project - README
===

# harmoniMix

## Table of Contents
1. [Overview](#Overview)
1. [Product Spec](#Product-Spec)
1. [Wireframes](#Wireframes)
2. [Schema](#Schema)

## Overview
### Description

Allows anybody to find songs and make music mashups and remixes. Utilizes the harmonic mixing wheel to determine what songs harmonically match with each other.
Start by searching for a base song. Choose the base song from the list of most likely results. If you don't see the song you want listed, it will search spotify and insert into database and redo that search with the new results. 
Otherwise, if it is there, then click that row and it uses that song as the base song for which the new list contains songs that harmonically harmonically match with it.

Nice to have: Being able to create your list of songs for mashup in house. Having a rating for how originally that mix is. Provide suggestions for mashup songs based on 4 input criteria - [genre, release_year, camelot, and bpm]. Show what other DJ's have made mashups with what songs and post them to the app for others to listen to (soundcloudish).

### App Evaluation
[Evaluation of your app across the following attributes]
- *Category:* Lifestyle (Music)
- *Story:* Making music like DJ's do without all the hassle of searching for songs
- *Market:* Anyone who wants to make music at home
- *Habit:* Used in the planning stage of music production

### 2. Screen Archetypes

- Home Screen - Main Search Page
- Stream1: Base Song List
  - User can view a list of most likely results of base song
- Stream2: Harmonic Song List
  - User can view list of songs harmonically matching to chosen base song
- Stream3: Adding to Song List For Songs Not in DB on Base Song List Search
  - User can click a button that pulls data from spotify
