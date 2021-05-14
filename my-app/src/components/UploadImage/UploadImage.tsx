import React, {useState} from "react";
import {Button, ButtonToolbar, Icon, Panel, Uploader} from "rsuite";
import {FileType} from "rsuite/es/Uploader";
import axios from "axios";

const styles = {
    lineHeight: '5em',
}

const UploadImage = ({}) => {
    const [files, setFiles] = useState<FileType[]>([]);
    const [image, setImage] = useState<string>('')

    const upload = () => {
        const formData = new FormData();
        files.forEach(file => formData.append('files', file.blobFile!!, file.name))
        axios.post('http://127.0.0.1:5000/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }).then(res => console.log(res))
    }

    const getFile = () => {
        axios.get('http://127.0.0.1:5000/test', {responseType: 'arraybuffer'})
            .then(res => {
                const base64 = btoa(
                    new Uint8Array(res.data).reduce(
                        (data, byte) => data + String.fromCharCode(byte),
                        '',
                    ),
                );
                setImage("data:;base64," + base64);
            })
    }

    const clear = () => {
        setFiles([]);
    }

    return (
        <Panel shaded header={'Загрузите несколько изображений'}>
            <Uploader
                // action={'http://127.0.0.1:5000/upload'}
                name={'files'}
                accept={'image/jpeg,image/png,image/gif,image/tiff'}
                fileList={files}
                fileListVisible={true}
                onChange={(list) => setFiles(list)}
                draggable
                multiple
                listType={'picture-text'}
                autoUpload={false}
            >
                <div style={styles}>
                    <Icon icon='camera-retro' size="5x" style={{marginTop: '0.5em'}}/>
                    <p>Нажмите или перетащите</p>
                </div>
            </Uploader>
            <ButtonToolbar style={{marginTop: '2em'}}>
                <Button
                    appearance={'primary'}
                    onClick={upload}
                    disabled={files.length === 0}
                >
                    Отправить
                </Button>
                <Button
                    color={'red'}
                    onClick={clear}
                    disabled={files.length === 0}
                >
                    Очистить
                </Button>
            </ButtonToolbar>
            {image && <img src={image}/>}
        </Panel>
    )
}

export default UploadImage;