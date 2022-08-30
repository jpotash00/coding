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

### 3. Navigation

*Tab Navigation* (Tab to Screen)
- Base Song Search

*Flow Navigation* (Screen to Screen)

- Landing Search Page
  - => Stream1
- Stream1: Base Song List
  - => Stream2
  - => Stream3
- Stream2: Pull Data From Spotify & Insert Into Database
  - => Stream1
- Stream3: Harmonic Song List
  - => Stream1

## Schema
### Models

Songs

| Property     | Type       | Description                         |
| -------------| -----------| ----------------------------------- |
| song_id      | int        | unique id for song                  |
| title        | String     | name of song                        |
| artist       | String     | name of who wrote song              |
| genre        | String     | type of music song is               |
| released_year| int        | year song was released              |
| song_key     | String     | major musical note in song          |
| bpm          | int        | how fast/rhythmic the song is       |
| camelot      | String     | value of song_key based on wheel    |
| Instrumental_type| String | whether song is an instrumental or not|
| ranked      | int         | rank given based on search          |

### Networking

- Landing Page/Main Search Screen
- Stream1: Base Song List
  - (POST) Query "songlist" based on post value
- Stream2: Pull Data From Spotify & Insert Into Database
  - (Read/GET) Value from POST above
  - (POST) Query "spotify" based on retrieved value, inserted into database, and then search rerun  
- Stream3: Harmonic Song List
  - (Read/GET) Value from table row and Query "songlist" where camelot is row's camelot
  - (POST) Query "songlist" based on post value
