API_URL = 'https://tadata.me/csm/%s' # %s = imdb id

####################################################################################################
def Start():

	HTTP.CacheTime = CACHE_1WEEK

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

		try:
			json_obj = JSON.ObjectFromURL(API_URL % (metadata.id), sleep=2.0)
		except:
			Log("*** Failed retrieving data from %s"  % (API_URL % (metadata.id)))
			return None

		if 'error' in json_obj:
			Log('*** An error occurred: %s' % (json_obj['error']))
			return None

		# Content rating
		if json_obj['recommended_age']:
			metadata.content_rating = 'CSM %s' % (json_obj['recommended_age'])

		# Add short description as tagline
		if Prefs['add_tagline'] and json_obj['description']:
			metadata.tagline = json_obj['description']
		else:
			metadata.tagline = None

		# Add Common Sense Media review to reviews
		metadata.reviews.clear()

		if Prefs['add_review'] and json_obj['review']:

			review = metadata.reviews.new()
			review.source = 'Common Sense Media'
			review.text = json_obj['review']
