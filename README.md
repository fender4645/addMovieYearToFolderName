# addMovieYearToFolderName
A simple script that will take a folder name (assuming it's a movie name), lookup the year the movie was released, and rename to include the folder to include the year

I wrote this as I was transitioning from Couchpotato to Radarr. When you bulk import movies into Radarr, it expects that every movie is in it's own folder and that the folder name has the year the movie was released (e.g. "American Beauty (1999)"). All of my movie files were in nested folders but the folder names did not have the year in it which would cause Radarr to not import any of my movies.

In a nutshell, all this script does is:
<ol>
  <li>Looks inside a given folder for subfolders</li>
  <li>Takes the name of each folder (assuming that it's a movie title) and looks it up in The Movie Database to find its release year</li>
  <li>If it finds multiple years, you can either be prompted to select the year or you can just take the first one it finds</li>
  <li>It will rename the folder to include the selected date in the format: <Movie Title (year)>
    </ol>

## Requirements
<ol>
  <li>tmdbsimple</li>
  <li>A The Movie Database API key (can regestier for free at https://www.themoviedb.org</li>
</ol>

## Usage

  
