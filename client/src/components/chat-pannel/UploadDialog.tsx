import * as Dialog from '@radix-ui/react-dialog';
import {Cross2Icon} from '@radix-ui/react-icons';
import './styleUploadDialog.css';
import {Text} from "@radix-ui/themes";
import {StateUpdater} from "preact/hooks";
import {useRef} from "preact/compat";

function UploadDialog(props: { fileStorage: StateUpdater<File | null> }) {

    const ref = useRef<HTMLInputElement>(null);

    function FileUpload() {
        return (
            <div style={{
                width: "100%",
                height: "200px",
                backgroundColor: "transparent",
                border: "3px dashed var(--violet-5)",
                borderRadius: "5px",
                display: "flex",
                justifyContent: "center",
                alignItems: "center"

            }}>
                <input ref={ref} type="file" name="file" id="file" style={{
                    padding: "180px 20% ",
                }}/>
            </div>
        );
    }

    return (

        <Dialog.Root>
            <Dialog.Trigger asChild>
                <Text>Upload Media</Text>
            </Dialog.Trigger>
            <Dialog.Portal>
                <Dialog.Overlay className="DialogOverlay"/>
                <Dialog.Content className="DialogContent">
                    <Dialog.Title className="DialogTitle">Upload Media</Dialog.Title>
                    <Dialog.Description className="DialogDescription">
                        Upload your media here. Click save when you're done.
                    </Dialog.Description>
                    <FileUpload/>
                    <div style={{display: 'flex', marginTop: 25, justifyContent: 'flex-end'}}>
                        <Dialog.Close asChild>
                            <button className="Button green" onClick={() => {
                                console.log(ref?.current?.files)
                                props.fileStorage(ref?.current?.files ? ref.current.files[0] : null)
                            }}>Save
                            </button>
                        </Dialog.Close>
                    </div>
                    <Dialog.Close asChild>
                        <button className="IconButton" aria-label="Close">
                            <Cross2Icon/>
                        </button>
                    </Dialog.Close>
                </Dialog.Content>
            </Dialog.Portal>
        </Dialog.Root>
    );
}

export default UploadDialog;

