import dateFormat from 'dateformat'
import { History } from 'history'
import update from 'immutability-helper'
import * as React from 'react'
import {
  Button,
  Checkbox,
  Divider,
  Grid,
  Header,
  Icon,
  Input,
  Loader
} from 'semantic-ui-react'

import { createFile, deleteFile, getFiles, putFile } from '../api/fileUploadApi'
import Auth from '../auth/Auth'
import { File } from '../types/File'

interface FilesProps {
  auth: Auth;
  history: History;
}

interface FilesState {
  files: File[];
  newFilename: string;
  loadingFiles: boolean;
}

export class FileUploads extends React.PureComponent<FilesProps, FilesState> {
  state: FilesState = {
    files: [],
    newFilename: '',
    loadingFiles: true
  }

  handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    this.setState({ newFilename: event.target.value })
  }

  onEditButtonClick = (file_uuid: string) => {
    this.props.history.push(`/files/${file_uuid}/edit`)
  }

  onFileCreate = async (event: React.ChangeEvent<HTMLButtonElement>) => {
    try {
      const record_created = this.getCurrentTimestamp()
      const newFile = await createFile(this.props.auth.getIdToken(), {
        filename: this.state.newFilename,
        record_created
      })
      this.setState({
        files: [...this.state.files, newFile],
        newFilename: ''
      })
    } catch {
      alert('File creation failed')
    }
  }

  onFileDelete = async (file_uuid: string) => {
    try {
      await deleteFile(this.props.auth.getIdToken(), file_uuid)
      this.setState({
        files: this.state.files.filter(file => file.file_uuid != file_uuid)
      })
    } catch {
      alert('File deletion failed')
    }
  }

  onFileCheck = async (pos: number) => {
    try {
      const file = this.state.files[pos]
      await putFile(this.props.auth.getIdToken(), file.file_uuid, {
        filename: file.filename,
        uploaded: file.uploaded,
        record_created: file.record_created,
      })
      this.setState({
        files: update(this.state.files, {
          [pos]: { uploaded: { $set: true } }
        })
      })
    } catch {
      alert('File update failed')
    }
  }

  async componentDidMount() {
    try {
      const files = await getFiles(this.props.auth.getIdToken())
      this.setState({
        files,
        loadingFiles: false
      })
    } catch (e) {
      alert(`Failed to fetch files: ${e.message}`)
    }
  }

  render() {
    return (
      <div>
        <Header as="h1">File Upload</Header>

        {this.renderCreateFileInput()}

        {this.renderFiles()}
      </div>
    )
  }

  renderCreateFileInput() {
    return (
      <Grid.Row>
        <Grid.Column width={16}>
          <Input
            action={{
              color: 'teal',
              labelPosition: 'left',
              icon: 'add',
              content: 'New filename',
              onClick: this.onFileCreate
            }}
            fluid
            actionPosition="left"
            placeholder="My-new-file.pdf"
            onChange={this.handleNameChange}
          />
        </Grid.Column>
        <Grid.Column width={16}>
          <Divider />
        </Grid.Column>
      </Grid.Row>
    )
  }

  renderFiles() {
    if (this.state.loadingFiles) {
      return this.renderLoading()
    }

    return this.renderFilesList()
  }

  renderLoading() {
    return (
      <Grid.Row>
        <Loader indeterminate active inline="centered">
          Loading Files
        </Loader>
      </Grid.Row>
    )
  }

  renderFilesList() {
    console.log(`Files: ${this.state.files}`);
    return (
      <Grid padded>
        {this.state.files.map((file, pos) => {
          return (
            <Grid.Row key={file.file_uuid}>
              <Grid.Column width={1} verticalAlign="middle">
                <Checkbox
                  onChange={() => this.onFileCheck(pos)}
                  checked={file.favorite}
                />
              </Grid.Column>
              <Grid.Column width={10} verticalAlign="middle">
                {file.filename}
              </Grid.Column>
              <Grid.Column width={3} floated="right">
                {file.record_created}
              </Grid.Column>
              <Grid.Column width={1} floated="right">
                <Button
                  icon
                  color="blue"
                  onClick={() => this.onEditButtonClick(file.file_uuid)}
                >
                  <Icon name="pencil" />
                </Button>
              </Grid.Column>
              <Grid.Column width={1} floated="right">
                <Button
                  icon
                  color="red"
                  onClick={() => this.onFileDelete(file.file_uuid)}
                >
                  <Icon name="delete" />
                </Button>
              </Grid.Column>
              File uploaded: {file.uploaded}
              }
              <Grid.Column width={16}>
                <Divider />
              </Grid.Column>
            </Grid.Row>
          )
        })}
      </Grid>
    )
  }

  getCurrentTimestamp(): string {
    return dateFormat(new Date(), "AMERICANSHORTWTIME");
  }
}
