import * as Dialog from '@radix-ui/react-dialog';
import {Cross2Icon} from '@radix-ui/react-icons';
import './styleUploadDialog.css';
import {Text} from "@radix-ui/themes";
import {useRef} from "preact/compat";
import {ReviewApi, ReviewPost} from "../../api";

function ReviewDialog(props: { reviewAPI: ReviewApi, conversation_id: number, other_user_id: number }) {

    const ref = useRef<HTMLInputElement>(null);


    return (

        <Dialog.Root>
            <Dialog.Trigger asChild>
                <Text>Give a review</Text>
            </Dialog.Trigger>
            <Dialog.Portal>
                <Dialog.Overlay className="DialogOverlay"/>
                <Dialog.Content className="DialogContent">
                    <Dialog.Title className="DialogTitle">Upload Media</Dialog.Title>
                    <Dialog.Description className="DialogDescription">
                        Give your review here.
                    </Dialog.Description>
                    <fieldset className="Fieldset">
                        <label className="Label" htmlFor="review">
                            Review
                        </label>
                        <input ref={ref} className="Input" id="review"/>
                    </fieldset>
                    <div style={{display: 'flex', marginTop: 25, justifyContent: 'flex-end'}}>
                        <Dialog.Close asChild>
                            <button className="Button green" onClick={async () => {
                                if (ref.current?.value === undefined) return;
                                const review: ReviewPost = {
                                    personal: 10,
                                    working: 10,
                                    payment: 10,
                                    text: ref.current?.value ?? "",
                                    user: {
                                        user_id: props.other_user_id,
                                    }
                                }
                                await props.reviewAPI.createReviewReviewPost(review);
                            }}>
                                Save
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

export default ReviewDialog;

