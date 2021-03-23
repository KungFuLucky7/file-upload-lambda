import * as React from 'react'
import { Button, Form } from 'semantic-ui-react'
import Auth from '../auth/Auth'
import { getFile, getUploadUrl, uploadFileData } from '../api/fileUploadApi'

enum UploadState {
  NoUpload,
  FetchingPresignedUrl,
  UploadingFile,
}

interface EditFileProps {
  match: {
    params: {
      file_uuid: string
    }
  }
  auth: Auth
}

interface EditFileState {
  file: any
  uploadState: UploadState
}

export class EditFile extends React.PureComponent<
  EditFileProps,
  EditFileState
> {
  state: EditFileState = {
    file: undefined,
    uploadState: UploadState.NoUpload
  }

  handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (!files) return

    this.setState({
      file: files[0]
    })
  }

  handleSubmit = async (event: React.SyntheticEvent) => {
    event.preventDefault()

    try {
      if (!this.state.file) {
        alert('File should be selected')
        return
      }

      this.setUploadState(UploadState.FetchingPresignedUrl)
      const file_uuid = this.props.match.params.file_uuid;
      const file = await getFile(this.props.auth.getIdToken(), file_uuid);
      console.log("File:", file);
      const content_type = file.content_type;
      const uploadUrl = await getUploadUrl(this.props.auth.getIdToken(), file_uuid);
      this.setUploadState(UploadState.UploadingFile);
      await uploadFileData(uploadUrl, this.state.file, content_type);

      alert('File was uploaded!');
    } catch (e) {
      alert('Could not upload a file: ' + e.message);
    } finally {
      this.setUploadState(UploadState.NoUpload);
    }
  }

  setUploadState(uploadState: UploadState) {
    this.setState({
      uploadState
    })
  }

  render() {
    return (
      <div>
        <h1>Upload new file</h1>

        <Form onSubmit={this.handleSubmit}>
          <Form.Field>
            <label>File</label>
            <input
              type="file"
              accept="*/*"
              placeholder="File to upload"
              onChange={this.handleFileChange}
            />
          </Form.Field>

          {this.renderButton()}
        </Form>
      </div>
    )
  }

  renderButton() {

    return (
      <div>
        {this.state.uploadState === UploadState.FetchingPresignedUrl && <p>Uploading file metadata</p>}
        {this.state.uploadState === UploadState.UploadingFile && <p>Uploading file</p>}
        <Button
          loading={this.state.uploadState !== UploadState.NoUpload}
          type="submit"
        >
          Upload
        </Button>
      </div>
    )
  }
}
