import { Link } from 'react-router-dom'
const Welcome = () => {

    const content = (
        <section className="profile">
            <div className="profile-section">
                <h1>Profile and Statistics</h1>

                <p>Unique User Id: </p>

                <p>Email Address:</p>

                <p>Display Name: </p>
            </div>
            <div className="mastery-section">
                <h2>Mastery Statistics</h2>
                <div className="mastery-stats">
                    <label for="algebra">Algebra</label>
                    <p><progress id="algebra" value="0" max="100"></progress></p>
                    <label for="dataAnalysis">Data Analysis, Statistics, and Probability</label>
                    <p><progress id="dataAnalysis" value="0" max="100"></progress></p>
                    <label for="geometry">Geometry</label>
                    <p><progress id="geometry" value="0" max="100"></progress></p>
                    <label for="measurement">Measurement</label>
                    <p><progress id="measurement" value="0" max="100"></progress></p>
                    <label for="numberProperties">Number Properties and Operations</label>
                    <p><progress id="numberProperties" value="0" max="100"></progress></p>                </div>

                <Link to="/modules" className="btn btn-primary">Continue Learning</Link>
            </div>
        </section>
    )

    return content
}
export default Welcome