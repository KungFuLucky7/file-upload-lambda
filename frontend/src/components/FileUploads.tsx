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
  Image,
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

  onEditButtonClick = (fileUuid: string) => {
    this.props.history.push(`/files/${fileUuid}/edit`)
  }

  onFileCreate = async (event: React.ChangeEvent<HTMLButtonElement>) => {
    try {
      const dueDate = this.calculateDueDate()
      const newFile = await createFile(this.props.auth.getIdToken(), {
        name: this.state.newFilename,
        dueDate
      })
      this.setState({
        files: [...this.state.files, newFile],
        newFilename: ''
      })
    } catch {
      alert('File creation failed')
    }
  }

  onFileDelete = async (fileUuid: string) => {
    try {
      await deleteFile(this.props.auth.getIdToken(), fileUuid)
      this.setState({
        files: this.state.files.filter(todo => todo.fileUuid != fileUuid)
      })
    } catch {
      alert('Todo deletion failed')
    }
  }

  onFileCheck = async (pos: number) => {
    try {
      const file = this.state.files[pos]
      await putFile(this.props.auth.getIdToken(), file.fileUuid, {
        filename: file.filename,
        description: file.description,
        recordCreated: file.recordCreated,
      })
      this.setState({
        files: update(this.state.files, {
          [pos]: { description: { $set: file.description } }
        })
      })
    } catch {
      alert('Todo deletion failed')
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
        <Header as="h1">File Uploads</Header>

        {this.renderCreateTodoInput()}

        {this.renderFileUploads()}
      </div>
    )
  }

  renderCreateTodoInput() {
    return (
      <Grid.Row>
        <Grid.Column width={16}>
          <Input
            action={{
              color: 'teal',
              labelPosition: 'left',
              icon: 'add',
              content: 'New task',
              onClick: this.onTodoCreate
            }}
            fluid
            actionPosition="left"
            placeholder="To change the world..."
            onChange={this.handleNameChange}
          />
        </Grid.Column>
        <Grid.Column width={16}>
          <Divider />
        </Grid.Column>
      </Grid.Row>
    )
  }

  renderFileUploads() {
    if (this.state.loadingFiles) {
      return this.renderLoading()
    }

    return this.renderFileUploadsList()
  }

  renderLoading() {
    return (
      <Grid.Row>
        <Loader indeterminate active inline="centered">
          Loading TODOs
        </Loader>
      </Grid.Row>
    )
  }

  renderFileUploadsList() {
    return (
      <Grid padded>
        {this.state.files.map((todo, pos) => {
          return (
            <Grid.Row key={todo.fileUuid}>
              <Grid.Column width={1} verticalAlign="middle">
                <Checkbox
                  onChange={() => this.onTodoCheck(pos)}
                  checked={todo.done}
                />
              </Grid.Column>
              <Grid.Column width={10} verticalAlign="middle">
                {todo.name}
              </Grid.Column>
              <Grid.Column width={3} floated="right">
                {todo.dueDate}
              </Grid.Column>
              <Grid.Column width={1} floated="right">
                <Button
                  icon
                  color="blue"
                  onClick={() => this.onEditButtonClick(todo.fileUuid)}
                >
                  <Icon name="pencil" />
                </Button>
              </Grid.Column>
              <Grid.Column width={1} floated="right">
                <Button
                  icon
                  color="red"
                  onClick={() => this.onTodoDelete(todo.fileUuid)}
                >
                  <Icon name="delete" />
                </Button>
              </Grid.Column>
              {todo.attachmentUrl && (
                <Image src={todo.attachmentUrl} size="small" wrapped />
              )}
              <Grid.Column width={16}>
                <Divider />
              </Grid.Column>
            </Grid.Row>
          )
        })}
      </Grid>
    )
  }

  calculateDueDate(): string {
    const date = new Date()
    date.setDate(date.getDate() + 7)

    return dateFormat(date, 'yyyy-mm-dd') as string
  }
}
