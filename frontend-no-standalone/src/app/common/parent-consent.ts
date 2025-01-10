export class ParentConsent {
    id: number;
    parentUser: number;
    childUser: number;
    consent: number;
    isConsent: boolean;
    file: string;

    constructor(
        id: number,
        parentUser: number,
        childUser: number,
        consent: number,
        isConsent: boolean,
        file: string
    ) {
        this. id = id;
        this.parentUser = parentUser;
        this.childUser = childUser;
        this.consent = consent;
        this.isConsent = isConsent;
        this.file = file;
    }

    static fromApiResponse(response: any): ParentConsent {
        return new ParentConsent(
            response.id,
            response.parent_user,
            response.child_user,
            response.consent,
            response.is_consent,
            response.file
        );
    } 
}
