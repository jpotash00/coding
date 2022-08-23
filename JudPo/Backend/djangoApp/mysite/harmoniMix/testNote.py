#from views 

#---> raw query: 
# xyz = Songs.objects.raw("select * from songs where song_id in %s", [strNum])







#---------------HTML
# {% load static %}
# <link rel="stylesheet" href="{% static 'style.css' %}" />

# <form action='songlist/' class="search-bar" pattern=".*/S.*" method="POST">  <!-- action has to be sent somewhere!-->
#   {% csrf_token %}
#   <!-- {{form}} -->
#   <input class="form" type="text" required="required" name="song" placeholder="Search for songs by title, artist, or by title & artist">  <!-- need search info containing valid searches-->
#   <button class="search-btn" type="submit">
#       <span>Search</span>
#   </button>
# </form>
#----------------