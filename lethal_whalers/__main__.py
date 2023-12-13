from .api_client import ApiClient


def run():
    upload_modpack()


def upload_modpack():
    client = ApiClient()
    filename = "./modpack/modpack.zip"

    init_upload_response = client.user_media_initiate_upload(filename)
    upload_url = init_upload_response.upload_urls[0].url

    file_part = client.do_s3_upload(upload_url, filename)

    final_upload_response = client.user_media_finish_upload(
        uuid=init_upload_response.user_media.uuid, file_part=file_part
    )

    client.submit_submission(uuid=final_upload_response.uuid)


if __name__ == "__main__":
    run()
