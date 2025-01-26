package eu.tutorials.to_dolistapp

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import eu.tutorials.to_dolistapp.ui.theme.TodoListAppTheme
import java.util.Calendar

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            TodoListAppTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color.White
                ) {
                    TodoListScreen()
                }
            }
        }
    }
}

@Composable
fun TodoListScreen() {
    var taskText by remember { mutableStateOf("") }
    val tasks = remember { mutableStateListOf<Pair<String, Boolean>>() }
    val currentYear = Calendar.getInstance().get(Calendar.YEAR)

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        Text(
            text = "To-Do List",
            style = MaterialTheme.typography.headlineMedium,
            color = Color.Black,
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp), textAlign = TextAlign.Center
        )

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            BasicTextField(
                value = taskText,
                onValueChange = { taskText = it },
                modifier = Modifier
                    .weight(1f)
                    .padding(8.dp)
                    .height(56.dp)
                    .border(1.dp, MaterialTheme.colorScheme.primary, MaterialTheme.shapes.medium)
                    .padding(8.dp),
                textStyle = MaterialTheme.typography.bodyLarge.copy(Color.Black)
            )

            Button(onClick = {
                if (taskText.isNotBlank()) {
                    tasks.add(taskText to false)
                    taskText = ""
                }
            },colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF90EE90))
            ) {
                Text("Add")
            }
        }

        LazyColumn(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f),
            verticalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(tasks.size) { index ->
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .background(Color.LightGray, RoundedCornerShape(8.dp))
                        .padding(8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Checkbox(
                            checked = tasks[index].second,
                            onCheckedChange = { isChecked ->
                                tasks[index] = tasks[index].first to isChecked
                            }
                        )
                        Text(
                            text = tasks[index].first,
                            style = MaterialTheme.typography.bodyLarge,
                            modifier = Modifier.padding(start = 8.dp),
                            color = Color.Black
                        )
                    }

                    Button(
                        onClick = {
                            tasks.removeAt(index)
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF90EE90))
                    ) {
                        Text("Remove")
                    }
                }
            }
        }

        Button(
            onClick = { tasks.clear() },
            modifier = Modifier.align(Alignment.CenterHorizontally),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF90EE90))

        ) {
            Text("Clear All")
        }
        Spacer(modifier = Modifier.weight(0.1f))

        Text(
            text = "side_end.dev all rights reserved @$currentYear",
            style = MaterialTheme.typography.bodySmall,
            color = Color.Gray,
            modifier = Modifier.fillMaxWidth().padding(16.dp),
            textAlign = TextAlign.Center
        )
    }
}

