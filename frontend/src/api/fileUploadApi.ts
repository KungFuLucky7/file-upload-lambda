import { apiEndpoint } from '../config'
import { File } from '../types/File';
import { CreateFileRequest } from '../types/CreateFileRequest';
import Axios from 'axios'
import { UpdateFileRequest } from '../types/UpdateFileRequest';

export async function getFiles(idToken: string): Promise<File[]> {
  console.log('Fetching files')

  const response = await Axios.get(`${apiEndpoint}/files/metadata`, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${idToken}`
    },
  })
  console.log('Got files:', response.data);
  return response.data;
}

export async function createFile(
  idToken: string,
  newFile: CreateFileRequest
): Promise<File> {
  const response = await Axios.post(`${apiEndpoint}/files/metadata`,  JSON.stringify(newFile), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${idToken}`
    }
  })
  console.log('Created file:', response.data);
  return response.data;
}

export async function getFile(idToken: string, file_uuid: string): Promise<File[]> {
  console.log('Fetching a file')

  const response = await Axios.get(`${apiEndpoint}/files/metadata${file_uuid}`, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${idToken}`
    },
  })
  console.log('Got file:', response.data);
  return response.data;
}

export async function putFile(
  idToken: string,
  file_uuid: string,
  updatedFile: UpdateFileRequest
): Promise<void> {
  const response = await Axios.put(`${apiEndpoint}/files/metadata/${file_uuid}`, JSON.stringify(updatedFile), {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${idToken}`
    }
  })
  console.log('Updated file:', response.data);
  return response.data;
}

export async function deleteFile(
  idToken: string,
  file_uuid: string
): Promise<void> {
  await Axios.delete(`${apiEndpoint}/files/metadata/${file_uuid}`, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${idToken}`
    }
  })
  console.log('Deleted file:', file_uuid);
}

export async function getUploadUrl(
  idToken: string,
  file_uuid: string
): Promise<string> {
  const response = await Axios.post(`${apiEndpoint}/files/${file_uuid}`, '', {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${idToken}`
    }
  })
  console.log('Upload URL:', response.data);
  return response.data;
}

export async function uploadFileData(uploadUrl: string, file: Buffer): Promise<void> {
  await Axios.put(uploadUrl, file)
}

export async function downloadFileData(
  idToken: string,
  file_uuid: string
): Promise<string> {
  const response = await Axios.get(`${apiEndpoint}/files/${file_uuid}`, {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${idToken}`
    }
  })
  console.log('Download URL:', response.data);
  return response.data
}
