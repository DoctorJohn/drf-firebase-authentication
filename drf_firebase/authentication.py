from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from firebase_admin import auth as firebase_auth

class BaseFirebaseAuthentication(authentication.BaseAuthentication):
	"""
	Firebase Authentication based django restframework authentication class.

	Clients should authenticate by passing a Firebase ID Token in the
	"Authorization" HTTP header, preprended with the string "<keyword> " where
	<keyword> is this classes `keyword` string property. For example:

	Authorization: FirebaseToken xxxxx.yyyyy.zzzzz
	"""
	keyword = 'FirebaseToken'
	check_revoked = False

	def authenticate(self, request):
		auth = authentication.get_authorization_header(request).split()

		if not auth or auth[0].lower() != self.keyword.lower().encode():
			return None

		if len(auth) == 1:
			msg = _('Invalid token header. No credentials provided.')
			raise AuthenticationFailed(msg)
		elif len(auth) > 2:
			msg = _('Invalid token header. Token string should not contain spaces.')
			raise AuthenticationFailed(msg)

		try:
			firebase_token = auth[1].decode()
		except UnicodeError:
			msg = _('Invalid token header. Token string should not contain invalid characters.')
			raise AuthenticationFailed(msg)

		return self.authenticate_credentials(firebase_token)

	def authenticate_credentials(self, firebase_token):
		try:
			decoded_token = firebase_auth.verify_id_token(
				firebase_token,
				app=self.get_firebase_app(),
				check_revoked=self.check_revoked,
			)
		except ValueError:
			# Token invalid, or the App's project ID cannot be determined.
			msg = _('The Firebase token was invalid.')
			raise AuthenticationFailed(msg)
		except firebase_auth.AuthError:
			msg = _('The Firebase token was revoked.')
			raise AuthenticationFailed(msg)

		firebase_uid = decoded_token['uid']
		firebase_user_record = firebase_auth.get_user(
			firebase_uid,
			app=self.get_firebase_app(),
		)

		# This template method must be implemented in a subclass.
		user = self.get_django_user(firebase_user_record)

		if user is None:
			msg = _('No matching local user found.')
			raise AuthenticationFailed(msg)

		return (user, firebase_token)

	def get_firebase_app(self):
		"""
		This method must be implemented in a subclass of this class. It must
		return a valid Firebase App instance.

		Firebase App docs:
		https://firebase.google.com/docs/reference/admin/python/firebase_admin#app
		"""
		msg = 'Implement this method in a subclass.'
		raise NotImplemented(msg)

	def get_django_user(self, firebase_user_record):
		"""
		Returns a django user associated with the requesting firebase user.

		As we don't know how you intent on associating a firebase user with
		your local django users, this method must be implemented in a subclass.

		This method takes a firebase UserRecord object as parameter. You may
		use its properties to find or create a local django user.

		Return None in case you want the authentication process to fail.
		eg. when the requesting users email address is not verified.

		Firebase UserRecord ocs:
		https://firebase.google.com/docs/reference/admin/python/firebase_admin.auth#userrecord
		"""
		msg = 'Implement this method in a subclass.'
		raise NotImplemented(msg)

	def authenticate_header(self, request):
		"""
		Returns a string that will be used as the value of the WWW-Authenticate
		header in a HTTP 401 Unauthorized response.
		"""
		return self.keyword