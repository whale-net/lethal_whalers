import os

import requests
from openapi_client.models.completed_part import CompletedPart
from openapi_client.models.user_media import UserMedia
from openapi_client.models.user_media_finish_upload_params import \
    UserMediaFinishUploadParams
from openapi_client.models.user_media_initiate_upload_params import \
    UserMediaInitiateUploadParams
from openapi_client.models.user_media_initiate_upload_response import \
    UserMediaInitiateUploadResponse

from openapi_client.models.package_submission_metadata import PackageSubmissionMetadata
from openapi_client.models.package_submission_result import PackageSubmissionResult

class ApiClient():
    """
    basic client
    """

    def __init__(self):
        self.__BASE_API_URL: str = 'https://thunderstore.io'
        self.__API_USER: str = os.environ.get('LETHAL_WHALER_API_USER')
        self.__API_PASSWORD: str = os.environ.get('LETHAL_WHALER_API_PASSWORD')

        # TODO session subclass https://stackoverflow.com/questions/42601812/python-requests-url-base-in-session
        self._session = requests.Session()
        self._session.headers.update({
            'accept': 'application/json', 
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.__API_PASSWORD}'
        })

    @staticmethod
    def _process_response(response: requests.Response) -> str:
        # TODO - error handling
        json_content = str(response.content, encoding='UTF-8')
        return json_content

    def user_media_initiate_upload(self, filename: str) -> UserMediaInitiateUploadResponse:

        if not os.path.exists(filename):
            raise(FileNotFoundError())
        file_size_bytes = os.path.getsize(filename)

        parm = UserMediaInitiateUploadParams(filename=filename, file_size_bytes=file_size_bytes)
        response = self._session.post(self.__BASE_API_URL + '/api/experimental/usermedia/initiate-upload/', data=parm.to_json())
        json_content = ApiClient._process_response(response=response)
        um_response = UserMediaInitiateUploadResponse.from_json(json_content)

        # printing because debugger requires setting env variables intelligently which I'm not bothering with (yet)
        # print(um_response)

        return um_response
    
    def user_media_finish_upload(self, uuid: str, file_part: CompletedPart) -> UserMedia:
        parm = UserMediaFinishUploadParams(parts=[file_part])

        url = self.__BASE_API_URL + f'/api/experimental/usermedia/{uuid}/finish-upload/'

        response = self._session.post(url, parm.to_json())
        json_content = ApiClient._process_response(response=response)
        media = UserMedia.from_json(json_content)

        return media


    @staticmethod
    def do_s3_upload(upload_url: str, filename: str) -> CompletedPart:
        # 400 - not required so idc
        # options_resp = requests.options(upload_url)
        # print(options_resp.headers)

        with open(filename, 'rb') as file:
            # don't use session, it's different API entirely
            resp = requests.put(upload_url, file)

        # ETag = EntityTag which is from header - used to finalize submission
        etag = resp.headers['etag']

        # assuming 1 always will work, can pick up from upload_start response if needed
        part = CompletedPart(ETag=etag, PartNumber=1)
        return part
    
    def submit_submission(self, uuid: str) -> PackageSubmissionResult:
        parms = PackageSubmissionMetadata(
            upload_uuid=uuid,
            author_name='whale_net', # TODO CONFIGURABLE?
            #categories=['modpacks'],
            communities=['lethal-company'],
            categories=[],
            community_categories={'lethal-company': ["modpacks"]},
            has_nsfw_content=False,
        )

        response = self._session.post(self.__BASE_API_URL + '/api/experimental/submission/submit/', parms.to_json())
        print(response.content)