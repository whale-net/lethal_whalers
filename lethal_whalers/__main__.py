import os

import click

from .api_client import ApiClient
from .manifest_manager import Manifest

@click.group()
def cli():
    pass

@click.command()
def update_manifest():
    """
    Update manifest json to have current patch
    """
    manifest_path = './modpack/manifest.json'
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(manifest_path)
    json_data: bytes
    with open(manifest_path, 'rb') as manifest_file:
        json_data = manifest_file.read()
    manifest = Manifest.model_validate_json(json_data)

    patch_version = os.environ.get('COMMIT_COUNT')
    manifest.update_version(major=1, minor=1, patch=patch_version)

    out_json_data = manifest.model_dump_json(indent=True)
    with open(manifest_path, 'w') as manifest_file:
        manifest_file.write(out_json_data)
    print(patch_version)
    print(out_json_data)
    
@click.command()
def upload_modpack():
    """
    Upload modpack to Thunderstore
    """
    client = ApiClient()
    filename = "./modpack/modpack.zip"

    init_upload_response = client.user_media_initiate_upload(filename)
    upload_url = init_upload_response.upload_urls[0].url

    file_part = client.do_s3_upload(upload_url, filename)

    final_upload_response = client.user_media_finish_upload(
        uuid=init_upload_response.user_media.uuid, file_part=file_part
    )

    #print(final_upload_response)
    client.submit_submission(uuid=final_upload_response.uuid)


cli.add_command(update_manifest)
cli.add_command(upload_modpack)

if __name__ == "__main__":
    cli()
