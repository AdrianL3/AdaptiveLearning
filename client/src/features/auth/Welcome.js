import { Link } from 'react-router-dom'
const Welcome = () => {
    const date = new Date()
    const today = new Intl.DateTimeFormat('en-US', { dateStyle: 'full', timeStyle: 'long' }).format(date)

    const content = (
        //Add and edit the HTML here for the welcome page
        <section className="welcome">
            
            <p>{today}</p>

            <h1>Welcome!</h1>

            <p><Link to="/dash/questions">Questions</Link></p>

            <p><Link to="/dash/statistics">View Statistics</Link></p>

        </section>
    )

    return content
}
export default Welcome