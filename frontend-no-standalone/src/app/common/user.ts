export class User {
    id: number | null;
    first_name: string;
    last_name: string;
    username: string;
    email: string;
    phone_number: string | null;
    photo_url: string | null;
    birth_date: string;
    role: string;
    sex: string;
    status: string;

    constructor(data: Partial<User> = {}) {
    this.id = data.id || null;
    this.first_name = data.first_name || '';
    this.last_name = data.last_name || '';
    this.username = data.username || '';
    this.email = data.email || '';
    this.phone_number = data.phone_number || null;
    this.photo_url = data.photo_url || null;
    this.birth_date = data.birth_date || '';
    this.role = data.role || '';
    this.sex = data.sex || '';
    this.status = data.status || '';
    }
}
