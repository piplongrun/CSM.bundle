import certifi
import requests

VERSION = '3.2'
API_URL = 'https://api.tadata.me/csm/v2/?imdb_id=%s' # %s = imdb id

HTTP_HEADERS = {
	"User-Agent": "CSM/%s (%s %s; Plex Media Server %s)" % (VERSION, Platform.OS, Platform.OSVersion, Platform.ServerVersion)
}

####################################################################################################
def Start():

	pass

####################################################################################################
class CommonSenseMediaAgent(Agent.Movies):

	name = 'Common Sense Media'
	languages = [Locale.Language.NoLanguage]
	primary_provider = False
	contributes_to = [
		'com.plexapp.agents.imdb',
		'com.plexapp.agents.themoviedb'
	]

	def search(self, results, media, lang):

		if media.primary_agent == 'com.plexapp.agents.imdb':

			imdb_id = media.primary_metadata.id

		elif media.primary_agent == 'com.plexapp.agents.themoviedb':

			# Get the IMDb id from the Movie Database Agent
			imdb_id = Core.messaging.call_external_function(
				'com.plexapp.agents.themoviedb',
				'MessageKit:GetImdbId',
				kwargs = dict(
					tmdb_id = media.primary_metadata.id
				)
			)

			if not imdb_id:
				Log("*** Could not find IMDb id for movie with The Movie Database id: %s ***" % (media.primary_metadata.id))
				return None

		results.Append(MetadataSearchResult(
			id = imdb_id,
			score = 100
		))

	def update(self, metadata, media, lang):

		r = requests.get(API_URL % (metadata.id), headers=HTTP_HEADERS, verify=certifi.where())

		if 'error' in r.json():
			Log("*** An error occurred: %s ***" % (r.json()['error']))

			if Prefs['set_unrated'] and r.json()['error'] == 'No matches found.':
				metadata.content_rating = 'CSM Unrated'

			return

		# Content rating
		if r.json()['recommended_age']:
			metadata.content_rating = 'CSM %s' % (r.json()['recommended_age'])
		elif Prefs['set_unrated']:
			metadata.content_rating = 'CSM Unrated'
		else:
			metadata.content_rating = None

		# Add short description as tagline
		if Prefs['add_tagline'] and r.json()['description']:
			metadata.tagline = r.json()['description']
		else:
			metadata.tagline = None
