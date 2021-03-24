

def get_registration_name_and_link(user: User):
    temporary_token = TemporaryToken.objects.create(
        user=user,
        expires_dt=timezone.now() + timezone.timedelta(minutes=15)
    )
    query_string = temporary_token.query_string

    return user.first_name, f'{config.CLIENT_URL}/registration{query_string}'
